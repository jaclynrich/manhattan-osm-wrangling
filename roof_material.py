#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:29:32 2017

@author: Jackie
"""

from auditing import get_unexpected_counts
from pprint import pprint

file = 'lower_manhattan.osm.xml'

# tag key = roof:material
expected_roof_materials = ['acrylic_glass', 'concrete', 'eternit', 'plastic',
                           'asphalt', 'glass', 'grass', 'gravel', 'metal',
                           'plants', 'roof_tiles', 'shadecloth', 'slate',
                           'stone', 'tar_paper', 'thatch', 'wood']

# brick, copper, stainless_steel were deemed acceptable
roof_material_mapping = {'concrete;grass' : 'grass'}

if __name__ == '__main__':
    pprint(get_unexpected_counts(file, 'roof:material', expected_roof_materials))