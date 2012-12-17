#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request, make_response, jsonify
from os import environ
from datetime import datetime
import os
import csv

app = flask.Flask(__name__)
app.debug = True
LOG_FILE = 'serverlog.txt'
LOG_FILE_PATH = '/home/arenold/webarch253/server/logs/'
LOG_COOKIES = 'cookielog.txt'
TRENDING_URLS_FILE = 'trending_urls_script.csv'
TRENDING_URLS_FILE_PATH = '/home/arenold/webarch253/server/mrjob/' 

## open csv log file, log (cookie_id,datetime,action,User Agent)
## Actions 
## 1. main - access main page
## 2. create - create a short link
## 3. autocreate - autocreate a short link
## 4. delete - delete a link
## 5. redirect - visit a short link

## stores short as key:value short:url
db = shelve.open("shorten.db")

## stores clicks as key:value short:int clicks
clicks = shelve.open("clicks.db") 

def get_cookie_val():
    try:
        log = open(LOG_FILE_PATH + LOG_COOKIES,'r')
    except IOError:
	return app.logger.debug("cookie log file not found at "+ LOG_FILE_PATH+LOG_COOKIES)    
    
    csv_reader = csv.reader(log)

    for line in csv_reader:
        last_cookie = line[0] 
    log.close()

    next_cookie = int(last_cookie) + 1

    try:
        log = open(LOG_FILE_PATH + LOG_COOKIES,'a')
    except IOError:
        return app.logger.debug("cookie log file not found at "+ LOG_FILE_PATH+LOG_COOKIES)

    csv_writer = csv.writer(log)
    csv_writer.writerow([next_cookie,str(datetime.now())])
    log.close()

    return next_cookie

def write_log(logline):
    
    try:
        log = open(LOG_FILE_PATH + LOG_FILE,'a')
    except IOError:
        return app.logger.debug("log file not found at "+ LOG_FILE_PATH+LOG_FILE)

    csv_writer = csv.writer(log)
    csv_writer.writerow(logline)
    log.close()

@app.route('/')
def index():
    """index page for link shortener"""
    
    link_user = request.cookies.get('linkuser')
    user_browser = request.user_agent.browser
    time_stamp = datetime.now()
    action = "main"
    url = ""
    short = "" 
    lat = ""
    longitude = ""

    if link_user != None:
        #app.logger.debug("known client")
        logline = [str(time_stamp), link_user, user_browser, action, url, short, lat, longitude]
        #app.logger.debug(logline)
        write_log(logline)
        resp = make_response(flask.render_template('index.html'))
        return resp

    else:
        #app.logger.debug("unknown client")
        link_user = get_cookie_val()
        logline = [str(time_stamp), link_user, user_browser, action, url, short, lat, longitude ]
        #app.logger.debug(logline)
        write_log(logline)
        resp = make_response(flask.render_template('index.html'))
        resp.set_cookie('linkuser', link_user)
        return resp

###
# Now we'd like to do this generally:
# <short> will match any word and put it into the variable =short= Your task is
# to store the POST information in =db=, and then later redirect a GET request
# for that same word to the URL provided.  If there is no association between a
# =short= word and a URL, then return a 404
##/
@app.route("/create", methods=['PUT', 'POST'])
def create():
    """Create an association of =short= with the POST arguement =url="""
    link_user = request.cookies.get('linkuser')
    user_browser = request.user_agent.browser
    time_stamp = datetime.now()
    action = "create" ## create or autocreate? add a request param.
    lat = request.form['lat']
    longitude = request.form['long'] 

    if request.method == 'POST':
        url = request.form['url']
        short = request.form['short']

        ## add http:// if not in url
        if url.find('http://') == -1: 
            app.logger.debug("adding http://")
            url = 'http://' + url
	
        ## log user action
        logline = [str(time_stamp), link_user, user_browser, action, url, short, lat, longitude ]
        app.logger.debug(logline)
        write_log(logline)	

        ## check if url in db
        for shortDB, urlDB in db.items():
            if url == urlDB or url[:7] +'www.'+ url[7:] == urlDB:
                short = shortDB
                app.logger.debug(url+" already stored at "+ short)
                return jsonify(url=url,short=short,link="http://people.ischool.berkeley.edu/~arenold/server/"+short)
		
		## store new short and url
        app.logger.debug("request to store new "+url+" at "+short)
        clicks[str(short)] = 0 
        db[str(short)] = str(url)
	
        return jsonify(url=url,short=short,link="http://people.ischool.berkeley.edu/~arenold/server/"+short)
	
@app.route("/<short>", methods=['GET'])
def redirect(short):
    """Redirect the request to the URL associated =short=, otherwise return 404
    NOT FOUND"""
    link_user = request.cookies.get('linkuser')
    user_browser = request.user_agent.browser
    time_stamp = datetime.now()
    action = "redirect"
    lat = ""
    longitude = ""

    if link_user == None:
        link_user = get_cookie_val()

    if str(short) in db:
        url = db.get(str(short),'/')
        clicks[str(short)] += 1
        app.logger.debug("Redirecting to " + url + " with clicks " + str(clicks[str(short)]))
        
        ## log user action
        logline = [str(time_stamp), link_user, user_browser, action, url, short, lat, longitude ]
        write_log(logline)

        return flask.redirect(url)
    else:
        ## log user action
        logline = [str(time_stamp), link_user, user_browser, action, "404", short ]
        write_log(logline)

        return flask.render_template('404.html',short=short), 404

@app.route("/<short>", methods=['DELETE'])
def destroy(short):

    link_user = request.cookies.get('linkuser')
    user_browser = request.user_agent.browser
    time_stamp = datetime.now()
    action = "delete"
    lat = ""
    longitude = ""

    if str(short) in db:
        removed = db.pop(str(short))
        numClicks = clicks.pop(str(short))
        app.logger.debug("deleted " + removed + " with " + str(numClicks))

                ## log user action
        logline = [str(time_stamp), link_user, user_browser, action, removed, short, lat, longitude ]
        write_log(logline)

        return "deleted stored short " + removed
    else:
                ## log user action
        logline = [str(time_stamp), link_user, user_browser, action, "404", short ]
        write_log(logline)

        app.logger.debug("short "+short+" not in db")
        return flask.render_template('index.html'), 404
    	
@app.route("/123456789a", methods=['GET'])
def shorts():
    """return two dict of array short:url and array dict of short:clicks"""
    return jsonify(db=db.items(),clicks=clicks.items())

@app.route("/trending_urls", methods=['GET'])
def trending_urls():

    trending_file = open(TRENDING_URLS_FILE_PATH + TRENDING_URLS_FILE, 'r')
    trending = []

    for line in trending_file:
        for row in csv.reader([line]):
            for short, url in db.items():
                if url == row[0] or row[0][:7] +'www.'+ row[0][7:] == url:
                     trending.append({'url': row[0],'short': short,'clicks': row[1]})           

    return(jsonify(trending_urls=trending))

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
