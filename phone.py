#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 16:15:53 2017

@author: Jackie
"""

import re
from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'

def is_valid_phone(phone):
    r = re.compile(r'^\+1-\d{3}-\d{3}-\d{4}$')
    if r.match(phone) is not None:        
        return True
    else:
        return False

def update_phone(phone):
    """Returns the cleaned version of the phone number, and only returns
    the first phone number listed"""
    # replace multiple spaces with one space
    phone = re.sub('\s+', '', phone).strip()
    for ch in ['(',')','.','-']:
        phone = phone.replace(ch, '')
    
    if phone.startswith('001'):
        phone = '+' + phone[2:]
    if not phone.startswith('+'):
        phone = '+' + phone
    if phone[1] != '1':
        phone = phone[0] + '1' + phone[1:]
    
    phone = phone[0:2] + '-' + phone[2:5] + '-' + phone[5:8] + '-' + phone[8:]
    
    # Do not return second phone numbers or extensions
    phone = phone[0:15]
    
    if is_valid_phone(phone):
        return phone
    else:
        return None

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'phone', []))
    
    
    
    