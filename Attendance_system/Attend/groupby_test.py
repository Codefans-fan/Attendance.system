# -*- coding: utf-8 -*-
'''
Created on Apr 7, 2016

@author: fky
'''

import datetime
import itertools

use_date = ['2015-09-05 08:00:00',
            '2015-10-05',
            '2015-11-05',
            '2015-12-05',
            '2016-09-05',
            '2015-09-06',
            '2015-09-06',
            '2015-09-07',
            '2015-09-07']

date_objs = [datetime.datetime.now() for x in range(100)]

test = [list(group) for k, group in itertools.groupby(date_objs,key=lambda args: args.strftime('%Y-%m-%d'))]

for i in  test:
    print i
