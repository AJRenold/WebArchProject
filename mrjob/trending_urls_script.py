#!/usr/bin/env python
'''
tredning_urls_script.py reads the serverlog.txt file and outputs the url and the count
of the number of redirects going to that url for the current day only. *Counts redirects only for the current
date*

run like so:
	 python trending_urls_script.py

this MapReduce can be run ever hour to update the trending urls on our webpage!

'''
import csv
import os
from sys import stdout
from trending_urls import TrendingUrls
from datetime import datetime

def main(file_path = '/home/arenold/webarch253/server/logs/serverlog.txt'):

    save_file = 'trending_urls_script.csv'

    try:
        os.remove(save_file)
    except:
        pass

    top_urls = []
    top_urls_mr = TrendingUrls(args=[file_path])
    with top_urls_mr.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            url,visits = top_urls_mr.parse_output_line(line)
            top_urls.append((visits,url))

    top_urls.sort()
    top_urls.reverse()

    new_output_file = open(save_file,'w')

    csv_writer = csv.writer(new_output_file)
    for visits,url in top_urls:
        csv_writer.writerow([url,visits])

if __name__ == '__main__':
    main()

