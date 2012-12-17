#!/usr/bin/env python

from mrjob.job import MRJob
from csv_helper import csv_readline
from datetime import datetime,timedelta

class TrendingUrls(MRJob):

    def mapper(self,line_no,line):
        cell = csv_readline(line)
        if cell[3] == 'redirect':
            today = str(datetime.today())
            today = datetime.strptime(today[0:10],"%Y-%m-%d")
            log_date = datetime.strptime(cell[0][0:10],"%Y-%m-%d")
            if today == log_date:   
            	yield cell[4],1

    def reducer(self,url,count):
        yield url,sum(count)

if __name__ == '__main__':
    TrendingUrls.run()

