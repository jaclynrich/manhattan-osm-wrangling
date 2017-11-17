#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 11:57:14 2017

@author: Jackie

Functions for auditing the data
"""

import xml.etree.cElementTree as ET
import re

file = 'lower_manhattan.osm.xml'

def get_tag_key_counts(filename):
    """ Returns a count of all of the different keys for tags"""
    keys = {}
    for _, elem in ET.iterparse(filename, events=('start',)):
        if elem.tag == 'tag':
            keys[elem.attrib['k']] = keys.get(elem.attrib['k'], 0) + 1
    return keys

# There are no tags with PROBLEMCHARS
tags = get_tag_key_counts(file)
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
for tag in tags:
    if PROBLEMCHARS.match(tag):
        print(tag)

def get_unexpected_counts(filename, key, valid_list):
    """ Returns the counts of all of the unexpected values for a particular
    tag key.  Use an empty list as valid_list to return all of the values"""
    attrib_counts = {}
    for _, elem in ET.iterparse(filename, events=('start',)):
        if elem.tag == 'tag':
            value = elem.attrib['v'].strip()
            if elem.attrib['k'] == key and value not in valid_list:
                attrib_counts[value] = attrib_counts.get(value, 0) + 1
    return attrib_counts

def get_non_numeric(filename, key):
    """ Returns the non-numeric values for a particular tag key"""
    non_num = []
    for _, elem in ET.iterparse(filename, events=('start',)):
        if elem.tag == 'tag':
            if elem.attrib['k'] == key:
                try:
                    float(elem.attrib['v'])
                except ValueError:
                    if elem.attrib['v'] is not None:
                        non_num.append(elem.attrib['v'])
    return non_num