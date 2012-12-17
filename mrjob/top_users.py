#!/usr/bin/env python

from mrjob.job import MRJob
from csv_helper import csv_readline


class TopUsers(MRJob):

    def mapper(self,user,line):
        cell = csv_readline(line)
        if cell[3] == 'main':
            yield cell[1],1

    def reducer(self,user,count):
        yield user,sum(count)

if __name__ == '__main__':
    TopUsers.run()

