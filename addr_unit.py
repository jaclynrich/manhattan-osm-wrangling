#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:17:28 2017

@author: Jackie
"""
import re
from auditing import get_non_numeric
from pprint import pprint

file = 'lower_manhattan.osm.xml'    

def change_addr_unit_key(unit):
    floor_m = re.search('floor', unit, re.IGNORECASE)
    suite_m = re.search('suite', unit, re.IGNORECASE)
    if floor_m:
        return 'addr:floor'
    if suite_m:
        return 'addr:suite'
    else:
        pass

def update_addr_unit(unit):
    m = re.findall('(\d+)', unit)
    return m[0]

if __name__ == '__main__':
    pprint(get_non_numeric(file, 'addr:unit'))