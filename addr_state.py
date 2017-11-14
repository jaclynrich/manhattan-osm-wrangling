#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 16:11:41 2017

@author: Jackie
"""
from auditing import get_unexpected_counts
import pprint

file = 'lower_manhattan.osm.xml'

valid_state = 'NY'

if __name__ == '__main__':
    pprint.pprint(get_unexpected_counts(file, 'addr:state', valid_state))