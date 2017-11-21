#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:52:55 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'    

def update_addr_district(district):
    return None

# Soho is not an official district
if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'addr:district', []))