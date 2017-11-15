#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:53:50 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

file = 'lower_manhattan.osm.xml'

# Get acceptable values from osm wiki
url = 'http://wiki.openstreetmap.org/wiki/Key:leisure'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

official_leisure = set()
for s in soup.findAll('a', href=re.compile('^/wiki/Tag:leisure')):
    official_leisure.add(s.text.strip())
official_leisure = list(official_leisure)

# social_club is an acceptable key
# values and the key that they need to be remapped to
leisure_key_mapping = {'recreation_ground': 'landuse'}

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'leisure', official_leisure))