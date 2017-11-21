#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:13:37 2017

@author: Jackie
"""

from auditing import get_non_numeric
from pprint import pprint

file = 'lower_manhattan.osm.xml'    

addr_floor_mapping = {'2nd': '2'}

if __name__ == '__main__':
    pprint(get_non_numeric(file, 'addr:floor'))