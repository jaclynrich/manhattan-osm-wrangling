#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:11:31 2017

@author: Jackie
"""
from auditing import get_unexpected_counts, get_non_numeric
from pprint import pprint

file = 'lower_manhattan.osm.xml'

#%%
# Tag keys that only require a simple mapping function to clean

# tag key = height
height_mapping = {'20ft' : '6.1',
                  '8ft' : '2.4',
                  '7ft' : '2.1',
                  '10ft' : '3.0',
                  
                  # multiple buildings should be described with building:part
                  # since height is defined as the max height
                  '14.8; 16.8; 14.8; 16.8; 15.2' : '16.8'}

# tag key = min_height
min_height_mapping = {'5;5.5' : '5'}

# tag key = nycdoitt:bin
nycdoitt_bin_mapping = {'1010604; 1083193; 1010604; 1083193; 1083194': '1083193'}

# tag key = building:part
building_part_mapping = {'#7F7E79': None,
                         'column': None,
                         'no': None,
                         'works': None}

#%%
def clean_with_mapping(value, mapping):
    """ Returns the cleaned version of the value, after using the mapping"""
    if value in mapping.keys():
        return mapping[value]
    return value

def get_key(value, key, key_mapping):
    """ Returns the key for the given value.  Some values may need to be
    reassigned to a different key according to the key mapping."""
    # return corrected key if necessary
    if value in key_mapping:
        return key_mapping[value]
    else:
        return key

#%%
if __name__ == '__main__':
    pprint(get_non_numeric(file, 'height'))
    pprint(get_non_numeric(file, 'min_height'))
    pprint(get_non_numeric(file, 'nycdoitt:bin'))
    pprint(get_unexpected_counts(file, 'building:part'))
