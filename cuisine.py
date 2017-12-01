#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:45:31 2017

@author: Jackie
"""

import re
from auditing import get_unexpected_counts
from pprint import pprint
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

file = 'lower_manhattan.osm.xml'

url = 'http://wiki.openstreetmap.org/wiki/Key:cuisine'

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Get the official cuisines from the wiki
not_include = ['fish', 'vegan', 'vegetarian']
official_cuisines = []
for table in soup.findAll('table', attrs={'class': re.compile(r'^wikitable')}):
    for a in table.findAll('a', attrs={'title': re.compile(r'^Tag:cuisine=')}):
        if a.text.strip() not in not_include:
            official_cuisines.append(a.text.strip())

# User defined values are also accepted, and I found those below to be
# appropriate cuisines
acceptable = ['austrian', 'belgian', 'breakfast', 'brunch', 'bubble_tea',
              'buffet', 'cajun', 'cambodian', 'cheesesteak', 'creole',
              'cuban', 'dim_sum', 'english', 'ethiopian', 'falafel',
              'filipino', 'grilled_cheese', 'hotdog', 'ice_pops', 'irish', 
              'israeli', 'juice', 'macaroni_and_cheese', 'matcha',
              'middle_eastern', 'moroccan', 'nepalese','new_american',
              'persian', 'peruvian', 'popcorn',  'pretzel', 'salad',
              'scandinavian', 'serbian','smoothie', 'southern',
              'southwestern','swiss', 'taco', 'taiwanese', 'ukrainian',
              'venezuelan', 'waffle']

# Add acceptable to official_cuisines
official_cuisines.extend(acceptable)

#%% Mapping and updating

# Full sequence values that mapped initially with no other subsequent mapping
full_mapping = {'italian coffee, breads, lite meals': ['italian', 'coffee_shop']}

fix_spacing_mapping = {'wine bar': 'wine_bar'}

# cuisine values that need to be mapped to a different key and possibly value
cuisine_key_mapping = {'pub': {'amenity': 'pub'},
                       'deli': {'shop': 'deli'},
                       'bakery': {'shop': 'bakery'},
                       'gastropub': {'amenity': 'restaurant'},
                       'vegan': {'diet:vegan': 'yes'},
                       'vegetarian': {'diet:vegetarian': 'yes'},
                       'cafe': {'amenity': 'cafe'},
                       'wine_bar': {'amenity': 'wine_bar'},
                       'fast_food': {'amenity': 'fast_food'},
                       'bar': {'amenity': 'bar'}}

# cuisine values that need to be mapped to a different value
cuisine_mapping = {'paletas': None,
                   'sweets': 'dessert',
                   'subs': 'sandwich',
                   'lobster_rolls': 'seafood',
                   'bagles': 'bagel',
                   'diner': None,
                   'bagels': 'bagel',
                   'sandwiches': 'sandwich',
                   'brasilian': 'brazilian',
                   'peruvian_chicken': ['peruvian','chicken'],
                   'spainish': 'spanish',
                   'steak': 'steak_house',
                   'arabic': 'arab',
                   'japanese_bakery': ['japanese','bakery'],
                   'donuts': 'donut',
                   'oysters': 'seafood',
                   'america': 'american',
                   'coffee': 'coffee_shop',
                   'tater_tots': None,
                   'irish_pub': 'irish',
                   'pan': None, # is part of pan-asian, so ignore pan
                   'tacos': 'taco',
                   'noodles': 'noodle',
                   'pita': 'mediterranean',
                   'ramen': 'noodle',
                   'pretzels': 'pretzel',
                   'matcha_bar': 'matcha',
                   'fish': 'seafood',
                   'creperie': 'crepe',
                   'medeteranian': 'mediterranean',
                   'taco_stand': 'taco',
                   'italian_pizza': ['italian','pizza'],
                   'salads': 'salad',
                   'wraps': 'sandwich',
                   'grill': 'barbecue',
                   'fine_dining': None,
                   'juiçe': 'juice',
                   'french_fries': 'friture',
                   'chinese_soup_dumplings': 'chinese',
                   'trattoria': 'italian',
                   'cuban_sandwich': ['cuban', 'sandwich'],
                   'cheese_steaks': 'cheesesteak',
                   'sliders': 'burger'}

def update_cuisine(cuisine):
    full_cuisines = []

    if cuisine in full_mapping:
        for val in full_mapping[cuisine]:
            full_cuisines.append({'cuisine': val})
        return full_cuisines
    
    if cuisine in fix_spacing_mapping:
        cuisine = fix_spacing_mapping[cuisine]
    
    # Split each cuisine, and for each cuisine find the mapping in the 
    # appropriate dictionary and append it to full_cuisines list
    res = re.split('\W+', cuisine)
    for r in res:
        r = re.sub('^_','', r).lower()
        if r in official_cuisines:
            full_cuisines.append({'cuisine': r})
        elif r in cuisine_mapping:
            map_val = cuisine_mapping[r]
            if isinstance(map_val, list):
                for mv in map_val:
                    full_cuisines.append({'cuisine': mv})
            elif map_val is not None:
                full_cuisines.append({'cuisine': map_val})
        elif r in cuisine_key_mapping:
            full_cuisines.append(cuisine_key_mapping[r])
    return full_cuisines

#%%
if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'cuisine_1', official_cuisines))
    cuisines = get_unexpected_counts(file, 'cuisine', official_cuisines)

    lower_c = {}
    for key, value in cuisines.items():
        lower_c[key.lower()] = value
    
    lower_unexpected = [c for c in lower_c if c not in official_cuisines]
    pprint(lower_unexpected)