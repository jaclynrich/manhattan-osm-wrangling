#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:13:41 2017

@author: Jackie
"""

from auditing import get_non_numeric
from pprint import pprint

file = 'lower_manhattan.osm.xml'

# Feet were converted to meters
# values that need to have their key reassigned and the correct key
capacity_key_mapping = {'Mon-Sun 17:00–23:00 Mon-Fri 12:00–15:30': 'opening_hours'}

capacity_mapping = {'56 seats': '56',
                    'Mon-Sun 17:00–23:00 Mon-Fri 12:00–15:30': \
                    'Su-Mo 17:00–23:00; Mo-Fr 12:00–15:30'}

if __name__ == '__main__':
    pprint(get_non_numeric(file, 'capacity'))