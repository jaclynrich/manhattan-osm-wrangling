#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:11:31 2017

@author: Jackie
"""
from auditing import get_unexpected_counts, print_non_numeric_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'

#%%
# Tag keys that only require a simple mapping function to clean

# tag key = height
pprint(print_non_numeric_counts(file, 'height'))
height_mapping = {'20ft' : '6.1',
                  '8ft' : '2.4',
                  '7ft' : '2.1',
                  '10ft' : '3.0',
                  
                  # multiple buildings should be described with building:part
                  # since height is defined as the max height
                  '14.8; 16.8; 14.8; 16.8; 15.2' : '16.8'}

# tag key = min_height
pprint(print_non_numeric_counts(file, 'min_height'))
min_height_mapping = {'5;5.5' : '5'}

# tag key = nycdoitt:bin
pprint(print_non_numeric_counts(file, 'nycdoitt:bin'))
nycdoitt_bin_mapping = {'1010604; 1083193; 1010604; 1083193; 1083194': '1083193'}

#%%
def clean_with_mapping(field, mapping):
    """ Returns the cleaned version of the field value, after using the mapping"""
    if field in mapping.keys():
        return mapping[field]
    return field