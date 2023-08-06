# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, '..')

from libawstatscleanup import CleanAwStats

testdir = '/home/trytproj/projekt/packages/mdsawstatscleanup/awstatscleanup/example/files'

# create testfiles
del_list = []
if os.path.exists(testdir):
    for y in range(3):
        year = y + 2017
        for m in range(12):
            fname = 'awstats%02d%04d.www.foo.bar.txt' % (m + 1, year)
            fpath = os.path.join(testdir, fname)
            
            fhdl = open(fpath, 'w')
            fhdl.write(fname)
            fhdl.close()

            del_list.append(fpath)


# run cleanup
ob1 = CleanAwStats(statsdir=testdir, keep_month=6)
ob1.runCleanup()

del ob1
