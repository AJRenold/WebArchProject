#!/usr/bin/env python
'''
top_users_script.py reads the serverlog.txt file and outputs the users (cookie id)
and the sum of their visits to the website. Counts only visits to main page.
Not redirects,create,deletes

run like so:
	 python top_users_script.py > top_users_script.out

'''
import csv
from sys import stdout
from top_users import TopUsers

def main(file_path = '/home/arenold/webarch253/server/logs/serverlog.txt'):

    top_users = []
    top_users_mr = TopUsers(args=[file_path])
    with top_users_mr.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            user,visits = top_users_mr.parse_output_line(line)
            top_users.append((visits,user))

    top_users.sort()
    top_users.reverse()

    csv_writer = csv.writer(stdout)
    for visits,user in top_users:
        csv_writer.writerow([user,visits])

if __name__ == '__main__':
    main()

