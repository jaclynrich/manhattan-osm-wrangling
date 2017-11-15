#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 22:23:27 2017

@author: Jackie
"""

from csv import DictWriter
import codecs
import pprint
import xml.etree.cElementTree as ET
import cerberus
import schema

# Cleaning functions and variables
from addr_postcode import update_postcode
from cleaning import clean_w_map, height_mapping, min_height_mapping, \
    nycdoitt_bin_mapping, get_key, building_part_mapping, \
    building_levels_mapping
from addr_city import update_city
from building import building_key_mapping, building_mapping
from roof_material import roof_material_mapping
from building_material import building_material_mapping
from highway import highway_mapping
from capacity import capacity_key_mapping, capacity_mapping
from amenity import amenity_key_mapping, amenity_mapping
from leisure import leisure_key_mapping
from shop import shop_key_mapping, shop_mapping

OSM_PATH = 'lower_manhattan.osm.xml'

NODES_PATH = 'output/nodes.csv'
NODE_TAGS_PATH = 'output/nodes_tags.csv'
WAYS_PATH = 'output/ways.csv'
WAY_NODES_PATH = 'output/ways_nodes.csv'
WAY_TAGS_PATH = 'output/ways_tags.csv'
RELATIONS_PATH = 'output/relations.csv'
RELATION_TAGS_PATH = 'output/relation_tags.csv'
RELATION_MEMBERS_PATH = 'output/relation_members.csv'

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in
# the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset',
               'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
RELATIONS_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
RELATION_TAG_FIELDS = ['id', 'key', 'value']
RELATION_MEMBER_FIELDS = ['id', 'type', 'node_id', 'role', 'position']

#%%
def shape_element(element, node_attr_fields=NODE_FIELDS,
                  way_attr_fields=WAY_FIELDS,
                  rel_attr_fields = RELATIONS_FIELDS):
    """Clean and shape node, way, relation XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    rel_attribs = {}
    rel_members = []
    tags = []  # Handle secondary tags the same way nodes, ways, relations

    if element.tag == 'node':
        for attrib in node_attr_fields:
            if element.get(attrib):
                node_attribs[attrib] = element.attrib[attrib]
            else:
                return
        
        for tag in element.iter('tag'):
            node_tags = {}
            node_tags['id'] = element.attrib['id']
            
            key = tag.attrib['k']
            value = tag.attrib['v']
            
            if key == 'addr:postcode':
                node_tags['value'] = update_postcode(value)
            elif key == 'height':
                node_tags['value'] = clean_w_map(value, height_mapping)
            elif key == 'min_height':
                node_tags['value'] = clean_w_map(value, min_height_mapping)
            elif key == 'nycdoitt:bin':
                node_tags['value'] = clean_w_map(value, nycdoitt_bin_mapping)
            elif key == 'addr:city':
                node_tags['value'] = update_city(value)
            elif key == 'addr:state':
                # No need for function, NY is the only valid value
                node_tags['value'] = 'NY'
            elif key == 'addr:country':
                # No need for function, US is the only valid value
                node_tags['value'] = 'US'
            elif key == 'building':
                key = get_key(value, key, building_key_mapping)
                node_tags['value'] = clean_w_map(value, building_mapping)
            elif key == 'roof:material':
                node_tags['value'] = clean_w_map(value, roof_material_mapping)
            elif key == 'building:material':
                node_tags['value'] = clean_w_map(value, building_material_mapping)
            elif key == 'highway':
                node_tags['value'] = clean_w_map(value, highway_mapping)
            elif key == 'capacity':
                key = get_key(value, key, capacity_key_mapping)
                node_tags['value'] = clean_w_map(value, capacity_mapping)
            elif key == 'amenity':
                key = get_key(value, key, amenity_key_mapping)
                node_tags['value'] = clean_w_map(value, amenity_mapping)
            elif key == 'building:part':
                node_tags['value'] = clean_w_map(value, building_part_mapping)
            elif key == 'leisure':
                key = get_key(value, key, leisure_key_mapping)
            elif key == 'shop':
                key = get_key(value, key, shop_key_mapping)
                node_tags['value'] = clean_w_map(value, shop_mapping)
            elif key == 'building:levels':
                node_tags['value'] = clean_w_map(value, building_levels_mapping)
            else:
                node_tags['value'] = value
            
            node_tags['key'] = key
            
            # Skip any values that are None
            if node_tags['value'] == None:
                continue
            else:
                tags.append(node_tags)
            
            # Additional key and values to append
            node_tags = {}
            id_num = element.attrib['id']
            if id_num == '3056978842':
                node_tags['id'] = id_num
                node_tags['key'] = 'books'
                node_tags['value'] = 'comic'
            tags.append(node_tags)
            
        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        for attrib in way_attr_fields:
            if element.get(attrib):
                way_attribs[attrib] = element.attrib[attrib]
            else:
                return
        
        for tag in element.iter('tag'):
            way_tags = {}
            way_tags['id'] = element.attrib['id']
            
            key = tag.attrib['k']
            value = tag.attrib['v']
            
            if key == 'addr:postcode':
                way_tags['value'] = update_postcode(value)
            elif key == 'height':
                way_tags['value'] = clean_w_map(value, height_mapping)
            elif key == 'min_height':
                way_tags['value'] = clean_w_map(value, min_height_mapping)
            elif key == 'nycdoitt:bin':
                way_tags['value'] = clean_w_map(value, nycdoitt_bin_mapping)
            elif key == 'addr:city':
                way_tags['value'] = update_city(value)
            elif key == 'addr:state':
                # No need for function, NY is the only valid value
                way_tags['value'] = 'NY'
            elif key == 'addr:country':
                # No need for function, US is the only valid value
                way_tags['value'] = 'US'
            elif key == 'building':
                key = get_key(value, key, building_key_mapping)
                way_tags['value'] = clean_w_map(value, building_mapping)
            elif key == 'roof:material':
                way_tags['value'] = clean_w_map(value, roof_material_mapping)
            elif key == 'building:material':
                way_tags['value'] = clean_w_map(value, building_material_mapping)
            elif key == 'highway':
                way_tags['value'] = clean_w_map(value, highway_mapping)
            elif key == 'capacity':
                key = get_key(value, key, capacity_key_mapping)
                way_tags['value'] = clean_w_map(value, capacity_mapping)
            elif key == 'amenity':
                key = get_key(value, key, amenity_key_mapping)
                way_tags['value'] = clean_w_map(value, amenity_mapping)
            elif key == 'building:part':
                way_tags['value'] = clean_w_map(value, building_part_mapping)
            elif key == 'leisure':
                key = get_key(value, key, leisure_key_mapping)
            elif key == 'shop':
                key = get_key(value, key, shop_key_mapping)
                way_tags['value'] = clean_w_map(value, shop_mapping)
            else:
                way_tags['value'] = value

            way_tags['key'] = key 
           
            # Skip any values that are None
            if way_tags['value'] == None:
                continue
            else:
                tags.append(way_tags)

        i = 0
        for nd in element.iter('nd'):
            way_nd_dict = {}
            way_nd_dict['id'] = element.attrib['id']
            way_nd_dict['node_id'] = nd.attrib['ref']
            way_nd_dict['position'] = i
            way_nodes.append(way_nd_dict)
            i += 1

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
    
    elif element.tag == 'relation': 
        for attrib in rel_attr_fields:
            if element.get(attrib):
                rel_attribs[attrib] = element.attrib[attrib]
            else:
                return
        
        for tag in element.iter('tag'):
            rel_tags = {}
            rel_tags['id'] = element.attrib['id']
            
            key = tag.attrib['k']
            value = tag.attrib['v']
            
            if key == 'addr:postcode':
                rel_tags['value'] = update_postcode(value)
            elif key == 'height':
                rel_tags['value'] = clean_w_map(value, height_mapping)
            elif key == 'min_height':
                rel_tags['value'] = clean_w_map(value, min_height_mapping)
            elif key == 'nycdoitt:bin':
                rel_tags['value'] = clean_w_map(value, nycdoitt_bin_mapping)
            elif key == 'addr:city':
                rel_tags['value'] = update_city(value)
            elif key == 'addr:state':
                # No need for function, NY is the only valid value
                rel_tags['value'] = 'NY'
            elif key == 'addr:country':
                # No need for function, US is the only valid value
                rel_tags['value'] = 'US'
            elif key == 'building':
                key = get_key(value, key, building_key_mapping)
                rel_tags['value'] = clean_w_map(value, building_mapping)
            elif key == 'roof:material':
                rel_tags['value'] = clean_w_map(value, roof_material_mapping)
            elif key == 'building:material':
                rel_tags['value'] = clean_w_map(value, building_material_mapping)
            elif key == 'highway':
                rel_tags['value'] = clean_w_map(value, highway_mapping)
            elif key == 'capacity':
                key = get_key(value, key, capacity_key_mapping)
                rel_tags['value'] = clean_w_map(value, capacity_mapping)
            elif key == 'amenity':
                key = get_key(value, key, amenity_key_mapping)
                rel_tags['value'] = clean_w_map(value, amenity_mapping)
            elif key == 'building:part':
                rel_tags['value'] = clean_w_map(value, building_part_mapping)
            elif key == 'leisure':
                key = get_key(value, key, leisure_key_mapping)
            elif key == 'shop':
                key = get_key(value, key, shop_key_mapping)
                rel_tags['value'] = clean_w_map(value, shop_mapping)
            else:
                rel_tags['value'] = value
            
            rel_tags['key'] = key
            
            # Skip any values that are None
            if rel_tags['value'] == None:
                continue
            else:
                tags.append(rel_tags)

        i = 0
        for mem in element.iter('member'):
            rel_mem_dict = {}
            rel_mem_dict['id'] = element.attrib['id']
            rel_mem_dict['type'] = mem.attrib['type']
            rel_mem_dict['node_id'] = mem.attrib['ref']
            rel_mem_dict['role'] = mem.attrib['role']
            rel_mem_dict['position'] = i
            rel_members.append(rel_mem_dict)
            i += 1

        return {'relation': rel_attribs, 'relation_tags': tags, 
                'relation_members': rel_members}

#%%
        
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


# Main function
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csvs"""
    
    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file, \
         codecs.open(RELATIONS_PATH, 'w') as relations_file, \
         codecs.open(RELATION_TAGS_PATH, 'w') as rel_tags_file, \
         codecs.open(RELATION_MEMBERS_PATH, 'w') as rel_members_file:
             
             nodes_writer = DictWriter(nodes_file, fieldnames=NODE_FIELDS)
             node_tags_writer = DictWriter(nodes_tags_file, \
                                           fieldnames=NODE_TAGS_FIELDS)
             ways_writer = DictWriter(ways_file, fieldnames=WAY_FIELDS)
             way_nodes_writer = DictWriter(way_nodes_file, \
                                           fieldnames=WAY_NODES_FIELDS)
             way_tags_writer = DictWriter(way_tags_file, \
                                          fieldnames=WAY_TAGS_FIELDS)
             rel_writer = DictWriter(relations_file, \
                                     fieldnames=RELATIONS_FIELDS)
             rel_tags_writer = DictWriter(rel_tags_file, \
                                          fieldnames=RELATION_TAG_FIELDS)
             rel_members_writer = DictWriter(rel_members_file, \
                                             fieldnames=RELATION_MEMBER_FIELDS)
             
             nodes_writer.writeheader()
             node_tags_writer.writeheader()
             ways_writer.writeheader()
             way_nodes_writer.writeheader()
             way_tags_writer.writeheader()
             rel_writer.writeheader()
             rel_tags_writer.writeheader()
             rel_members_writer.writeheader()
             
             validator = cerberus.Validator()
             
             for element in get_element(file_in, tags=('node', 'way', 'relation')):
                 el = shape_element(element)
                 if el:
                     if validate is True:
                         validate_element(el, validator)
                     
                     if element.tag == 'node':
                         nodes_writer.writerow(el['node'])
                         node_tags_writer.writerows(el['node_tags'])
                     elif element.tag == 'way':
                         ways_writer.writerow(el['way'])
                         way_nodes_writer.writerows(el['way_nodes'])
                         way_tags_writer.writerows(el['way_tags'])
                     elif element.tag == 'relation':
                         rel_writer.writerow(el['relation'])
                         rel_tags_writer.writerows(el['relation_tags'])
                         rel_members_writer.writerows(el['relation_members'])

#%%                         

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower
    process_map(OSM_PATH, validate=False)
