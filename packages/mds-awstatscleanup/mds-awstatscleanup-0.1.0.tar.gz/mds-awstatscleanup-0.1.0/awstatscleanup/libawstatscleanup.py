# -*- coding: utf-8 -*-

import os
from datetime import date, timedelta

class CleanAwStats():

    def __init__(self, statsdir='/var/lib/awstats', keep_month=5):
        """ store values in class,
            statsdir: directory of statistics files,
            keep_month: number of months to keep, older stats will be removed
        """
        self.__statsdir = statsdir
        if os.path.exists(self.__statsdir) == False:
            raise ValueError('Directory "%s" dont exists' % self.__statsdir)
        self.__check_file_name(self.__statsdir)
        
        self.__keep_month = keep_month
        if not isinstance(self.__keep_month, type(1)):
            raise ValueError('parameter "keep_month" must be integer')
        if self.__keep_month <= 0:
            raise ValueError('parameter "keep_month" must positive')

    def __check_file_name(self, fname):
        """ allow absolute names only
        """
        if '*' in fname:
            raise ValueError('global sign in filename not allowd: "%s"' % fname)
        if '..' in fname:
            raise ValueError('relative path in filename not allowd: "%s"' % fname)
        if os.path.isabs(fname) == False:
            raise ValueError('path must be absolute: "%s"' % fname)
        if os.path.normpath(fname) != fname:
            raise ValueError('invalid path: "%s"' % fname)
        
    def __get_files(self):
        """ generate dict of files, sortetd by month
        """
        # get list of all files
        l1 = os.listdir(self.__statsdir)
        d1 = {}
        for i in l1:
            if i.startswith('awstats') and i.endswith('.txt'):
                p1 = len('awstats')
                m1 = int(i[p1:p1 + 2])
                y1 = int(i[p1 + 2:p1 + 6])
                
                dt1 = date(y1, m1, 1)
                if not dt1 in d1.keys():
                    d1[dt1] = []
                d1[dt1].append(i)
        return d1
        
    def __get_files_to_remove(self, files_dict):
        """ select files to remove
        """
        f_lst = []
        dt_limit = date.today()
        
        for i in range(self.__keep_month):
            dt_limit = date(dt_limit.year, dt_limit.month, 1)
            dt_limit -= timedelta(days=1)
        dt_limit = date(dt_limit.year, dt_limit.month, 1)

        for i in files_dict.keys():
            if i < dt_limit:
                f_lst.extend(files_dict[i])
        return f_lst
        
    def __removeFiles(self, files_to_remove):
        """ remove file in list
        """
        for i in files_to_remove:
            fname = os.path.join(self.__statsdir, i)
            self.__check_file_name(fname)
            if os.path.isfile(fname):
                os.remove(fname)

    def runCleanup(self):
        """ remove old statistics files
        """
        f_dict = self.__get_files()
        flst = self.__get_files_to_remove(f_dict)
        self.__removeFiles(flst)

# end CleanAwStats
