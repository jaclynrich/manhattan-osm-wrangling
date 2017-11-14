#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:01:32 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
import pprint

file = 'lower_manhattan.osm.xml'

valid_city_list = ['New York', 'Brooklyn']

# The title case version of the cities in the map
city_mapping = {'Manhattan Nyc': 'New York',
                'New York City': 'New York',
                'New York, Ny': 'New York',
                'Tribeca': 'New York',
                'York City': 'New York'
                }

def update_city(city, mapping=city_mapping, valid_list=valid_city_list):
    """ Returns the cleaned version of the postcode, after using the mapping"""
    city = city.title()
    if city in valid_city_list:
        return city
    else:
        return mapping[city]

if __name__ == '__main__':
    pprint.pprint(get_unexpected_counts(file, 'addr:city', valid_city_list))