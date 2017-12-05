#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 16:13:56 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'

addr_full_mapping = {'20 Jay Street #842, Brooklyn, New York 11201': None,
                     'Between 40th and 42nd Streets at 6th Avenue':
                         '6th Avenue between 40th and 42nd Streets'}
    
def get_additional_addr_full_tags(full):
    addtl_tags = {}
    if full == '20 Jay Street #842, Brooklyn, New York 11201':
        addtl_tags['addr:suite'] = '842'
    elif full == '42nd Street Between 7th Avenue and Broadway':
        addtl_tags['addr:housenumber'] = '1475'
        addtl_tags['addr:street'] = 'Broadway'
        addtl_tags['addr:city'] = 'New York'
        addtl_tags['addr:state'] = 'NY'
        addtl_tags['addr:postcode'] = '10036'
    return addtl_tags

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'addr:full', []))