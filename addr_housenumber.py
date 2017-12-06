#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 17:57:10 2017

@author: Jackie
"""

from auditing import get_non_numeric
from pprint import pprint
import re

file = 'lower_manhattan.osm.xml'

housenumber_mapping = {'9*9': None,
                       '54 2': None,
                       '162;157': '157,162',
                       '170, 176': '170,176',
                       '3rd Avenue': None,
                       'Level, 145': None}

acceptable = ['\d+', '\d+ 1/2', '\d+ 1/4', '\d+ 3/4', '\d+[a-zA-Z]',
              '\d+ Rear', '\d+-\d+', '\d+ Rear-[AB]', '\d+ Front [AB]',
              '\d+,\d+']

#%%

def apply_to_every_number(no):
    no = re.sub('REAR', 'Rear', no)
    if re.fullmatch('\d+ A', no):
        no = re.sub('\s', '', no)
    return no

def check_acceptable(no):
    tfs = []
    if no is not None:
        for a in acceptable:
            m = re.fullmatch(a, no)
            if m:
                tfs.append(True)
            else:
                tfs.append(False)
    if any(tfs):
        return True
    else:
        return False
    
    if any(tfs) or no is None:
        return no

def update_addr_housenumber(no):
    no = apply_to_every_number(no)
    if no in housenumber_mapping:
        no = housenumber_mapping[no]
    
    if check_acceptable(no) or no is None:
        return no
    else:
        # Those that do not match any of the regex have street info attached
        return no.split(' ', maxsplit=1)[0].replace(',', '')
    
def get_additional_housenumber_tags(no):
    addtl_tags = {}
    no = apply_to_every_number(no)
    
    mapping = {'9*9': None,
               '54 2': None,
               '162;157': '157,162',
               '170, 176': '170,176',
               '225 Varick':'225 Varick Street',
               '350 5th Ave': '350 5th Avenue'}
    
    has_full_street = ['1-3 Washington Square North', '502 9th Avenue',
                       '225 Varick Street', '350 5th Avenue']
    if no in mapping:
        no = mapping[no]
    
    if check_acceptable(no):
        return addtl_tags
    elif no is None:
        return addtl_tags
    else:
        if no == '3rd Avenue':
            addtl_tags['addr:street'] = '3rd Avenue'
            return addtl_tags
        if no == '408 West 22nd Street #2R':
            addtl_tags['addr:street'] = 'West 22nd Street'
            addtl_tags['addr:suite'] = '2R'
            return addtl_tags
        if no in has_full_street:
            addtl_tags['addr:street'] = no.split(' ', maxsplit=1)[1]
        if re.search('^Level', no):
            addtl_tags['addr:floor'] = re.findall('\d+', no)[0]
        if re.search('suite [\w]+', no):
            addtl_tags['addr:suite'] = re.findall('suite ([\w]+)', no)[0]
        if re.search('[\s]+[Ww]$', no):
            addtl_tags['direction'] = 'West'
        if re.search('West$', no):
            addtl_tags['direction'] = 'West'
        if re.search('[\s]+[EЕ]$', no):
            addtl_tags['direction'] = 'East'
        if re.search('East', no):
            addtl_tags['direction'] = 'East'
        return addtl_tags

#%%
if __name__ == '__main__':
    pprint(get_non_numeric(file, 'addr:housenumber'))