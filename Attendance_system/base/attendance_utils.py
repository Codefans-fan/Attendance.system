# -*- coding: utf-8 -*-
'''
Created on Apr 8, 2016

@author: fky
'''

import itertools

def _isnumeric(s):
    '''returns True if string s is numeric'''
    return all(c in "0123456789.+-" for c in s)


def filter_day_record(records,addHours=False):
    if records:
        res = []
        days_group =[list(group) for k, group in itertools.groupby(records,key=lambda args: args.lock_time.strftime('%Y-%m-%d'))]
        for grp in days_group:
            grp.sort(key=lambda p: p.lock_time)
            if len(grp) > 1:
                res.append(grp[0])
                res.append(grp[-1])
                if addHours:
                    timedalta =  grp[-1].lock_time - grp[0].lock_time
                    work_hours = float('%.2f'% (timedalta.total_seconds() / 3600))
                    if not grp[-1].comment.isdigit():
                        grp[-1].comment  = work_hours
                        grp[-1].save()
            else:
                res.append(grp[0])
        return res
    return []
    
def get_workHours(records):
    items = []
    for line in records:
        if _isnumeric(line.comment):
            items.append([float(line.lock_time.strftime('%H.%M')),float(line.comment)])
    return items


