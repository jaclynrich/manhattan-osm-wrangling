#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 16:29:45 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'addr:country', []))