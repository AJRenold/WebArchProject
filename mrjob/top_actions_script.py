#!/usr/bin/env python
'''
top_actions_script.py reads the serverlog.txt file and outputs the actions and
the sum of the number of actions.

run like so:
	 python top_actions_script.py > top_actions_script.out

'''
import csv
from sys import stdout
from top_actions import TopActions

def main(file_path = '/home/arenold/webarch253/server/logs/serverlog.txt'):

    actions = []
    top_actions_mr = TopActions(args=[file_path])
    with top_actions_mr.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            action,count = top_actions_mr.parse_output_line(line)
            actions.append((count,action))

    actions.sort()
    actions.reverse()

    csv_writer = csv.writer(stdout)
    for count,action in actions:
        csv_writer.writerow([action,count])

if __name__ == '__main__':
    main()

