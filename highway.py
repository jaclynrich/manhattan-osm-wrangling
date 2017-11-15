#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 06:57:41 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

file = 'lower_manhattan.osm.xml'

url = 'http://wiki.openstreetmap.org/wiki/Key:highway'

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
table = soup.find('table', class_='wikitable')

official_highways = set()
for tr in table.findAll('tr'):
    for a in tr.findAll('a', attrs={'title': re.compile(r'^Tag:highway=')}):
        official_highways.add(a.text.strip())
official_highways = list(official_highways)

# stop_line is a proposed feature and was deemed acceptable
# escalator can be described using highway=steps or =footway, but 
# there is no way to know which is appropriate
highway_mapping = {'escalator': None}

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'highway', official_highways))