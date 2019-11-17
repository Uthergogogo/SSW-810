"""
HW08
@author: Zeyu Wu
Date: 2019-10-21 12:48:13
"""
# !/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from prettytable import PrettyTable
import os
from collections import defaultdict


def date_arithmetic():
    """ return correct date tuple """
    date1 = datetime.strptime("Feb 27, 2000", "%b %d, %Y")
    date2 = datetime.strptime("Feb 27, 2017", "%b %d, %Y")
    date3 = datetime.strptime("Jan 1, 2017", "%b %d, %Y")
    date4 = datetime.strptime("Oct 31, 2017", "%b %d, %Y")
    num_days = 3
    dt1 = date1 + timedelta(days=num_days)
    dt2 = date2 + timedelta(days=num_days)
    delta = date4 - date3
    return dt1, dt2, delta


def file_reading_gen(path, fields, sep=',', header=False):
    """ read files and yield a tuple """
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"{path} not exist")
    else:
        with fp:
            row = 0
            if header:
                row += 1
                next(fp)
            for line in fp:
                this_line = line.strip().split(sep)
                total = len(this_line)
                row += 1
                if total != fields:
                    raise ValueError(f"{path} has {total} fields on line {row} but expected {fields}")
                yield tuple(this_line)


class FileAnalyzer:
    """ a class to analyze file """
    def __init__(self, directory):
        """ define attributes of the class """
        self.directory = directory  # NOT mandatory!
        self.files_summary = defaultdict(lambda: defaultdict(int))
        self.analyze_files()  # summarize the python files data

    def analyze_files(self):
        """ open file and count """
        try:
            files = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"Directory {self.directory} can't be found ")
        else:
            for file in files:
                try:
                    os.chdir(self.directory)
                    if os.path.isfile(file):  # handle with the situation if file is folder
                        fp = open(file, 'r')
                except FileNotFoundError:
                    raise FileNotFoundError(f"Can't open {file}")
                else:
                    if os.path.splitext(file)[1] == '.py':
                        with fp:
                            for line in fp:
                                self.files_summary[self.directory+'/'+file]['lines'] += 1  # count lines
                                self.files_summary[self.directory+'/'+file]['characters'] += len(line)  # count characters
                                if line.startswith('class '):  # count classes
                                    self.files_summary[self.directory+'/'+file]['classes'] += 1
                                if line.lstrip().startswith('def '):  # count functions
                                    self.files_summary[self.directory+'/'+file]['functions'] += 1

    def pretty_print(self):
        """ print the value by PrettyTable """
        pt = PrettyTable(field_names=['File name', 'Classes', 'Functions', 'Lines', 'Characters'])
        for file in self.files_summary.keys():
            pt.add_row([file,
                        self.files_summary[file]['classes'],
                        self.files_summary[file]['functions'],
                        self.files_summary[file]['lines'],
                        self.files_summary[file]['characters']])
        return pt



