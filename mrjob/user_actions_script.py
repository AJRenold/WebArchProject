#!/usr/bin/env python
'''
user_actions_script.py reads the serverlog.txt file and user id, the action
of the user (main,create,redirect,delete) and the count of the number of each
action for each user.

run like so:
	 python user_actions_script.py > user_actions_script.out

'''
import csv
from sys import stdout
from user_actions import UserActions

def main(file_path = '/home/arenold/webarch253/server/logs/serverlog.txt'):

    actions = []
    top_actions_mr = UserActions(args=[file_path])
    with top_actions_mr.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            user_action,count = top_actions_mr.parse_output_line(line)
            actions.append((count,user_action))

    actions.sort()
    actions.reverse()

    csv_writer = csv.writer(stdout)
    for count,user_action in actions:
        csv_writer.writerow([user_action[0],user_action[1],count])

if __name__ == '__main__':
    main()

