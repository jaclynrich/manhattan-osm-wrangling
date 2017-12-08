#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:02:45 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

file = 'lower_manhattan.osm.xml'

url = 'http://wiki.openstreetmap.org/wiki/Key:shop'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

shops = set()
for s in soup.findAll('a', href=re.compile('^/wiki/Tag:shop')):
    shops.add(s.text.strip())
shops = list(shops)

shop_key_mapping = {'car_rental': 'amenity',
                    'moving': 'office',
                    'shipping': 'amenity',
                    'tax': 'office'}

# Although shoe_repair is unexpected it is acceptable
shop_mapping = {'Medical Center' : None,
                'Video Production': None,
                'athletic': 'sports',
                'beer': 'alcohol',
                'comics': 'books',
                'creatures of comfort': None,
                'dry_cleaners;laundry': 'dry_cleaning',
                'general_stores': 'general',
                'handbags': 'bag',
                'home_goods': 'houseware',
                'market': None,
                'mattress': 'bed',
                'moving': 'moving_company',
                'nail_salon': 'beauty',
                'photography': 'art',
                'psychic': None,
                'shipping': 'post_office',
                'stationary': 'stationery',
                'tax': 'tax_advisory'}

def get_additional_shop_tags(shop):
    addtl_tags = {}
    if shop == 'comics':
        addtl_tags['books'] = 'comic'
    return addtl_tags

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'shop', shops))
    pprint(get_unexpected_counts(file, 'shop_1', shops))
