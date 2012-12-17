#!/usr/bin/env python

from mrjob.job import MRJob
from csv_helper import csv_readline


class TopActions(MRJob):

    def mapper(self,action,line):
        cell = csv_readline(line)
        yield cell[3], 1

    def reducer(self,action,count):
        yield action, sum(count)

if __name__ == '__main__':
    TopActions.run()

