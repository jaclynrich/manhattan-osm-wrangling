#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 13:39:22 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

file = 'lower_manhattan.osm.xml'

url = 'http://wiki.openstreetmap.org/wiki/Key:building'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
table = soup.find('table', class_='wikitable')

official_buildings = []
for tr in table.findAll('tr')[2:]:
    tds = tr.findAll('td')
    if len(tds) < 1:
        continue
    building = tds[1].text.strip()
    if building == 'user defined':
        break
    official_buildings.append(building)

# values that need to have their key reassigned and the correct key
building_key_mapping = {'college': 'amenity',
                        'convent': 'amenity',
                        'courthouse': 'amenity',
                        'fire_station': 'amenity',
                        'food_and_drink': 'amenity',
                        'library': 'amenity',
                        'theatre': 'amenity'}

# According to OSM wiki data_center is acceptable
building_mapping = {'no': None,
                    'publib': 'public',
                    'tower': None, # Neither are towers
                    'works': None,
                    'convent': 'monastery',
                    'food_and_drink': 'cafe'}

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'building', official_buildings))
    pprint(get_unexpected_counts(file, 'building_1', official_buildings))