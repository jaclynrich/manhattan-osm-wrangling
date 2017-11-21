#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:44:27 2017

@author: Jackie
"""

from auditing import get_unexpected_counts, get_non_numeric
from pprint import pprint
import re

file = 'lower_manhattan.osm.xml'

#%% roof:shape is already clean
roof_shapes = ['flat', 'skillion', 'gabled', 'half-hipped', 'hipped',
               'pyramidal', 'gambrel', 'mansard', 'dome', 'onion', 'round',
               'saltbox']
pprint(get_unexpected_counts(file, 'roof:shape', roof_shapes))

#%% building:colour
# all are clean - they are all either RGB hex or acceptable X11 colors

# print all values that are not RGB hex
colors = get_unexpected_counts(file, 'building:colour', [])
for c in colors:
    if not c.startswith('#'):
        print(c)

#%% roof:colour
# all are clean - they are all either RGB hex or acceptable X11 colors

# print all values that are not RGB hex
colours = get_unexpected_counts(file, 'roof:colour', [])
for c in colours:
    if not c.startswith('#'):
        print(c)

#%% oneway - already clean
oneway = ['yes', 'no', '-1', 'reversible', 'alternating']
pprint(get_unexpected_counts(file, 'oneway', oneway))

#%% maxspeeed
speeds = get_unexpected_counts(file, 'maxspeed', [])    
for speed in speeds:
    if not re.match('^\d+ mph$', speed):
        print(speed)

#%% addr:suite
pprint(get_non_numeric(file, 'addr:suite'))

#%% addr:level
pprint(get_non_numeric(file, 'addr:level'))

#%% addr:door
pprint(get_non_numeric(file, 'addr:door'))

#%% addr:interpolation
pprint(get_non_numeric(file, 'addr:interpolation'))

#%% delivery
pprint(get_unexpected_counts(file, 'delivery', ['no', 'yes']))