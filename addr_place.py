#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:50:32 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'    

addr_place_key_mapping = {'Hudson Street': 'addr:street'}

addr_place_mapping = {'Soho Mews': None,
                      'Manhattan Island': None}

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'addr:place', []))