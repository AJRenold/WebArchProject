#!/usr/bin/env python
'''
top_urls_script.py reads the serverlog.txt file and outputs the url and the count
of the number of redirects going to that url. *Counts redirects only*

run like so:
	 python top_urls_script.py > top_urls_script.out

'''
import csv
from sys import stdout
from top_urls import TopUrls

def main(file_path = '/home/arenold/webarch253/server/logs/serverlog.txt'):

    top_urls = []
    top_urls_mr = TopUrls(args=[file_path])
    with top_urls_mr.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            url,visits = top_urls_mr.parse_output_line(line)
            top_urls.append((visits,url))

    top_urls.sort()
    top_urls.reverse()

    csv_writer = csv.writer(stdout)
    for visits,url in top_urls:
        csv_writer.writerow([url,visits])

if __name__ == '__main__':
    main()

