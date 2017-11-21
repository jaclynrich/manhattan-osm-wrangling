#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 12:50:43 2017

@author: Jackie
"""

import re
from collections import defaultdict
from pprint import pprint
from auditing import get_unexpected_counts

file = 'lower_manhattan.osm.xml'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

    
invalid_streets = ['Washington Square Village', 'Track', '633', 
                   'Broadway Atrium', 'Grand Central Terminal',
                   'World Trade Center', 'World Financial Center',
                   'Gramercy Park']

expected = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Place',
            'Square', 'Lane', 'Road', 'Trail', 'Parkway', 'Commons', 'Way',
            'Terrace', 'Walk', 'A', 'B', 'C', 'D', 'Alley', 'Broadway',
            'Plaza', 'Center', 'Mews', 'Oval', 'Slip', 'Yards',  'Piers',
            'Heights', 'Green', 'Row', 'Loop', 'Americas', 'Finest', 'North',
            'West', 'South', 'East', 'Bowery', 'Line']

non_number_mapping = {'Second': '2nd',
                      'Third': '3rd',
                      'Fourth': '4th',
                      'Fifth': '5th',
                      'Seventh': '7th'}

full_street_mapping = {'85th West Street': 'West 85th Street',
                       '36th St Front 1': '36th Street',
                       '5th Ave 1807': '5th Avenue',
                       'West 27th': 'West 27th Street',
                       '29th': '29th Street',
                       'West 42nd': 'West 42nd Street',
                       'Highline': 'The High Line',
                       'Lafayette': 'Lafayette Street',
                       'Macdougal': 'MacDougal Street',
                       'Delancey Street Eb Roadbed': 'Delancey Street',
                       'Delancey St South': 'Delancey Street South',
                       'Warren': 'Warren Street',
                       'Bowery': 'The Bowery',
                       'Broadway.': 'Broadway',
                       'Old Fulton': 'Old Fulton Street',
                       'Macdougal Street': 'MacDougal Street',
                       'Mac Dougal Street': 'MacDougal Street',
                       'Mac Dougal Alley': 'MacDougal Alley',
                       'Park Ave S': 'Park Avenue South',                       
                       'La Guardia Place': 'LaGuardia Place',
                       'Laguardia Place': 'LaGuardia Place',
                       'West 30 Street': 'West 30th Street',
                       'West 31 Street': 'West 31st Street',
                       'East 12nd Street': 'East 12th Street',
                       'East 12 Street': 'East 12th Street',
                       'East 32th Street': 'East 32nd Street',
                       'East 33th Street': 'East 33rd Street',
                       'W 27th': 'West 27th Street',
                       'W 27 Street': 'West 27th Street',
                       'West 35 Street': 'West 35th Street',
                       'Saint Mark\'s Place': 'Saint Marks Place',
                       '110 Sixth Ave. At Watts St': '110 6th Avenue',
                       'State St & Water St': 'State Street & Water Street'}

street_type_mapping = {'Ave': 'Avenue',
                       'Avene': 'Avenue',
                       'St': 'Street',
                       'St.': 'Street',
                       'Steet': 'Street'}

#%% Formatting

def title_case(s, upper_exceptions, lower_exceptions):
    """ Returns the street with title capitalization """
    s = s.lower()
    parts = re.split('\s+', s)
    tc = []
    i = 0
    for p in parts:
        # ignore lower_exceptions if they are the first word
        if i == 0:
            if p in upper_exceptions:
                tc.append(p.upper())
            else:
                tc.append(p[0].upper() + p[1:])
        else:
            if p in lower_exceptions:
                tc.append(p)
            elif p in upper_exceptions:
                tc.append(p.upper())
            else:
                tc.append(p[0].upper() + p[1:])
        i += 1
    return(' '.join(tc))
    
def remove_commas(s):
    return s.replace(',', '')

#%% Floor

def has_floor(s):
    m = re.search('|'.join(['\d+\w* Floor', 'Floor \d+\w*']), s)
    if m:
        return True
    else:
        return False       

def extract_floor(s):
    m = re.findall('|'.join(['(\d+)\w* Floor', 'Floor (\d+)\w*']), s)
    for floor in m[0]:
        if floor != '':
            return floor
    else:
        return None

def remove_floor(s):
    if has_floor(s):
        m = re.search('|'.join(['\d+\w* Floor', 'Floor \d+\w*']), s)
        s = re.sub(m.group(), '', s)
    return s.strip()

#%% Suite
    
def has_suite(s):
    m = re.search("|".join(['Suite [\w]+', 'Ste\s[\w]+', '#[\w]+']), s)
    if m:
        return True
    else:
        return False
    
def extract_suite(s):
    m = re.findall("|".join(['Suite ([\w]+)', 'Ste\s([\w]+)', '#([\w]+)']), s)
    for suite in m[0]:
        if suite != '':
            return suite
    else:
        return None

def remove_suite(s):
    s = re.sub("|".join(['Suite [\w]+', 'Ste\s[\w]+', '#[\w]+']), '', s)
    return s.strip()

#%% Postcode
    
def has_postcode(s):
    m = re.search('(\d{5})', s) 
    if m:
        return True
    else:
        return False

def extract_postcode(s):
    return re.findall('(\d{5})', s) # gets five digits in a row

def remove_postcode(s):
    #if has_postcode(s):
        #m = re.search('(\d{5})', s) 
    s = re.sub('(\d{5})', '', s)
    return s.strip()

#%% City

def remove_city(s):
    if get_street_type(s) == 'Brooklyn':
        return s.replace('Brooklyn', '')
    return s.replace('New York, Ny', '')

#%% Housenumber
    
def has_housenumber(s):
    m = re.search('^\d+', s)
    if m:
        return True
    else:
        return False

def extract_housenumber(s):
    exceptions = ['14', '7']
    if has_housenumber(s):
        m = re.search('^\d+', s)
        if len(s.split()) == 4:
            return m.group()
        if len(s.split()) == 4 or (len(s.split()) == 3 and m.group() \
               not in exceptions):
            return m.group()
    else:
        return None
        
def remove_housenumber(s):
    if extract_housenumber(s) is not None:
        # Also find numbers with th
        m = re.search('^\d+[th]*', s)
        s = re.sub(m.group(), '', s)
    return s.strip()

#%% Find streets with middle numbers

def extract_middle_number(s):
    if s is not None:
        m = re.search('\d+ ', s)
        if m:
            print(' '.join(s, m.group()))

#%% Get non-number - numbered streets

def get_non_number(s):
    m = re.search('|'.join(['First', 'Second', 'Third', 'Fourth', 'Fifth',
                            'Sixth', 'Seventh', 'Eighth', 'Nineth', 'Tenth'
                            'Eleventh', 'Twelfth']), s)
    if m:
        return m.group()
    else:
        return None

def update_non_number(s):
    """ Return the numbered version of the non-number names for numbered
    streets"""
    if get_non_number(s) is not None:
        s = re.sub(get_non_number(s), non_number_mapping[get_non_number(s)], s)
    return s

#%% Find any Ats and &

def get_amps(s):
    m = re.search('&', s)
    if m:
        return m.group()
    else:
        return None

def get_ats(s):
    m = re.search(' At ', s)
    if m:
        return m.group()
    else:
        return None

#%% Auditing and cleaning

def get_street_type(street_name):
    street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
    if street_name is not None:
        m = street_type_re.search(street_name)
        if m:
            return m.group() 
        else:
            return None
    else:
        return None

def audit_street_type(street_types, street_name):
    street_type = get_street_type(street_name)
    if street_type is not None and street_type not in expected:
        street_types[street_type].add(street_name)

def update_street(s):
    s = title_case(s, ['fdr', 'un'], ['of', 'the'])

    if s in invalid_streets:
        return None
    if s in full_street_mapping:
        s = full_street_mapping[s]    
    
    s = remove_city(s)
    s = remove_commas(s)
    
    # Fix directional abbreviations
    s = re.sub('[\s]*W[\.]*[\s]+', ' West ', s).strip()
    s = re.sub('[\s]*E[\.]*[\s]+', ' East ', s).strip()
    s = re.sub('[\s]*S[\.]*$', ' South', s).strip()
    s = remove_floor(s)
    s = remove_suite(s)
    s = remove_postcode(s)
    s = remove_housenumber(s)
    s = update_non_number(s)
    
    st_type = get_street_type(s)
    if st_type in street_type_mapping:
        s = re.sub(st_type, street_type_mapping[st_type], s)
    return s.strip()

#%% Return a dictionary of the additional tags that are embedded in the street
    
def get_additional_tags(s):
    addtl_tags = {}
    if has_suite(s):
        addtl_tags['addr:suite'] = extract_suite(s)
    if has_postcode(s):
        addtl_tags['addr:postcode'] = extract_postcode(s)
    if get_street_type == 'Ny':
        addtl_tags['addr:city'] = 'New York'
    if get_street_type == 'Brooklyn':
        addtl_tags['addr:city'] = 'Brooklyn'
    if has_floor(s):
        addtl_tags['addr:floor'] = extract_floor(s)
    if has_housenumber(s):
        addtl_tags['addr:housenumber'] = extract_housenumber(s)
    return addtl_tags

#%%
if __name__ == '__main__':
    streets = get_unexpected_counts(file, 'addr:street', [])
    
    street_types = defaultdict(set)
    for s in streets:
        audit_street_type(street_types, s)

    for k, v in street_types.items():
        street_types[k] = list(v)
    pprint(street_types)