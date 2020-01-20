from html.parser import HTMLParser
from itertools import cycle

import time
import datetime

import os


class TableParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.table = []
        self.headers = []
        self.cycle_headers = []
        self.curr_row = {}
        self.curr_column = {}
        self.is_td = False
        self.is_th = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.is_td = True
            self.curr_column = next(self.cycle_headers)
            self.curr_row[self.curr_column] = ''
        elif tag == 'th':
            self.is_th = True

    def handle_data(self, data):
        if self.is_td:
            self.curr_row[self.curr_column] = data
        elif self.is_th:
            self.headers.append(data)

    def handle_endtag(self, tag):
        if tag == 'tr' and self.curr_row:
            self.table.append(self.curr_row)
            self.curr_row = {}
            self.curr_column = -1
        elif tag == 'td':
            self.is_td = False
        elif tag == 'th':
            self.is_th = False
            self.cycle_headers = cycle(self.headers)


if __name__ == '__main__':
    with open('report1512958667043.xls', encoding='utf-8') as f:
        content = f.read()
        table_parser = TableParser()
        table_parser.feed(content)
        for row in table_parser.table:
           # if float(row['Age (Hours)']) > 90 * 24:
           if time.strftime("%m/%d/%Y") - time.str(row['Closed Date'],"%m/%d/%Y") >90:
           			dir = "D:\\test\\" + row['Case Number']
                os.removedirs(dir)
                # delete folder here
