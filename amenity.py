#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:41:53 2017

@author: Jackie
"""
from auditing import get_unexpected_counts
from pprint import pprint
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

file = 'lower_manhattan.osm.xml'

url = 'http://wiki.openstreetmap.org/wiki/Key:amenity'

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
table = soup.find('table', class_='wikitable')

crossed_outs = ['firepit', 'gym', 'public_building', 'sauna']
official_amenities = []
for tr in table.findAll('tr', attrs={'id': re.compile(r'^amenity-')}):
    a = tr['id'][8:]
    if a == 'Proposed_features':
        break
    elif a in crossed_outs:
        pass
    else:
        official_amenities.append(a)
    
amenity_key_mapping = {'chiropractic': 'healthcare:specialty',
                       'clothing store': 'shop',
                       'disused': 'disused:amenity',
                       'gym': 'leisure',
                       'houseware': 'shop',
                       'nail_salon': 'shop',
                       'public_building': 'building',
                       'spa': 'shop',
                       'swimming_pool': 'leisure',
                       'urgent_care': 'healthcare:specialty'}

"""
The following unexpected values were deemed acceptable by the wiki: childcare,
ice_cream, money_transfer, parking_space
I think stock_exchange is acceptable
Note that car_service in the wiki means a place to get your car
serviced/repaired, but there is no acceptable value for a car hire
"""
amenity_mapping = {'car_service': None,
                   'clothing store': 'clothes',
                   'disused': 'restaurant',
                   'gym': 'fitness_centre',
                   'nail_salon': 'beauty',
                   'public_building': 'public',
                   'spa': 'beauty',
                   'urgent_care': 'emergency',
                   'training': 'school',
                   'wifi': None}
     
if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'amenity', official_amenities))
