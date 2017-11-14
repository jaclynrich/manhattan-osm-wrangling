#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 14:26:51 2017

@author: Jackie
"""
import re
from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'

# The following were manually collected zip codes that are within the 
# OSM map
valid_zip_list = ['10001', '10002', '10003', '10004', '10005', '10006', 
                  '10007', '10009', '10010', '10011', '10012', '10013', 
                  '10014', '10016', '10017', '10018', '10022', '10036',
                  '10038', '10045', '10048', '10110', '10118', '10121',
                  '10123', '10168', '10169', '10174', '10271', '10275',
                  '10280', '10281', '10282', '11201', '11205', '11211',
                  '11249', '11251']

# These specific zip codes were manually corrected
zip_mapping = {'100014': '10014',
               '10021': '10018',
               '10023': '10038'}

def update_postcode(postcode, mapping=zip_mapping, valid_list=valid_zip_list):
    """ Returns the cleaned version of the postcode, after using the mapping
    or finding 5 digits in a row in the string, and then ensures these new
    postcodes are in the valid_list"""
    if postcode in mapping.keys():
        return mapping[postcode]
    else:
        pc = re.findall('(\d{5})', postcode) # gets five digits in a row
        if len(pc) > 0:
            if pc[0] in valid_zip_list:
                return pc[0]
            elif pc[0] in mapping.keys():
                return mapping[pc[0]]
            else:
                return None
        else:
            return None

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'addr:postcode', valid_zip_list))