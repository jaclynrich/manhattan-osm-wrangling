#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 23:12:29 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

file = 'lower_manhattan.osm.xml'

url = 'http://wiki.openstreetmap.org/wiki/Key:building:material'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
table = soup.find('table', class_='wikitable')

official_b_materials = []
for tr in table.findAll('tr')[2:]:
    td = tr.findAll('td')[1]
    if not td.text.strip().startswith('?'):
        official_b_materials.append(td.text.strip())

# Although copper and granite were unexpected, they are still valid
building_material_mapping = {'40' : None}

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'building:material', official_b_materials))