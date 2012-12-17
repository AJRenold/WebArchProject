#!/usr/bin/env python

from mrjob.job import MRJob
from csv_helper import csv_readline


class TopUrls(MRJob):

    def mapper(self,line_no,line):
        cell = csv_readline(line)
        if cell[3] == 'redirect':
            yield cell[4],1

    def reducer(self,url,count):
        yield url,sum(count)

if __name__ == '__main__':
    TopUrls.run()

