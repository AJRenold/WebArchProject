#!/usr/bin/env python

from mrjob.job import MRJob
from csv_helper import csv_readline


class UserActions(MRJob):

    def steps(self):
        return [self.mr(self.user_action,self.action_list),self.mr(self.user_single_action,self.count_actions)]

    def user_action(self,line_no,line):
        cell = csv_readline(line)
        yield cell[1],cell[3]

    def action_list(self,user,actions):
        action_list = []
        for action in actions:
            action_list.append(action)
        yield user,action_list

    def user_single_action(self,user,action_list):
        for action in action_list:
            yield (user,action),1

    def count_actions(self,user_action,count):
        yield user_action,sum(count)

if __name__ == '__main__':
    UserActions.run()

