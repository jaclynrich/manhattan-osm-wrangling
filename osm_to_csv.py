#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 22:23:27 2017

@author: Jackie
"""

from csv import DictWriter
from pprint import pprint
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
from shop import shop_key_mapping, shop_mapping, get_additional_shop_tags
from phone import update_phone
from addr_street import update_street, get_additional_street_tags
from addr_place import addr_place_key_mapping, addr_place_mapping
from addr_floor import addr_floor_mapping
from addr_unit import change_addr_unit_key, update_addr_unit
from addr_district import update_addr_district
from cuisine import update_cuisine

OSM_PATH = 'lower_manhattan.osm.xml'

NODES_PATH = 'output_and_report/nodes.csv'
NODE_TAGS_PATH = 'output_and_report/nodes_tags.csv'
WAYS_PATH = 'output_and_report/ways.csv'
WAY_NODES_PATH = 'output_and_report/ways_nodes.csv'
WAY_TAGS_PATH = 'output_and_report/ways_tags.csv'
RELATIONS_PATH = 'output_and_report/relations.csv'
RELATION_TAGS_PATH = 'output_and_report/relations_tags.csv'
RELATION_MEMBERS_PATH = 'output_and_report/relations_members.csv'

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
            addtl_tags = []
            
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
                addtl_tags.append(get_additional_shop_tags(value))
            elif key == 'building:levels':
                node_tags['value'] = clean_w_map(value, building_levels_mapping)
            elif key == 'phone':
                node_tags['value'] = update_phone(value)
            elif key == 'Phone':
                key == 'phone'
                node_tags['value'] = update_phone(value)
            elif key == 'phone_1':
                key == 'phone'
                node_tags['value'] = update_phone(value)
            elif key == 'contact:phone':
                node_tags['value'] = update_phone(value)
            elif key == 'phone:emergency':
                node_tags['value'] = update_phone(value)
            elif key == 'fax':
                node_tags['value'] = update_phone(value)
            elif key == 'contact:fax':
                node_tags['value'] = update_phone(value)
            elif key == 'addr:street':
                node_tags['value'] = update_street(value)
                addtl_tags.append(get_additional_street_tags(value))
            elif key == 'addr:place':
                key = get_key(value, key, addr_place_key_mapping)
                node_tags['value'] = clean_w_map(value, addr_place_mapping)
            elif key == 'addr:floor':
                node_tags['value'] = clean_w_map(value, addr_floor_mapping)
            elif key == 'addr:unit':
                key = change_addr_unit_key(value)
                node_tags['value'] = update_addr_unit(value)
            elif key == 'addr:district':
                node_tags['value'] = update_addr_district(value)  
            elif key == 'building:level':
                key = 'building:levels'
                node_tags['value'] = value
            elif key == 'levels':
                key = 'level'
                node_tags['value'] = value
            elif key == 'addr:level':
                key = 'addr:floor'
                node_tags['value'] = value
            elif key == 'cuisine' or key == 'cuisine_1':
                addtl_tags.extend(update_cuisine(value))
            else:
                node_tags['value'] = value
            
            node_tags['key'] = key
            
            # Additional key and values to append
            for t in addtl_tags:
                for key, val in t.items():
                    addtl_tag = {}
                    addtl_tag['id'] = element.attrib['id']
                    addtl_tag['key'] = key
                    addtl_tag['value'] = val
                    if val is not None:
                        tags.append(addtl_tag)
            
            # Skip any values that are None
            if node_tags.get('value') is None:
                continue
            elif node_tags.get('key') is None or node_tags.get('key') == '':
                continue
            elif not isinstance(node_tags.get('value'), str):
                print(node_tags)
            else:
                tags.append(node_tags)
            
        # Make sure that there are no duplicates in tags
        unique_tags = [i for n, i in enumerate(tags) if i not in tags[n + 1:]]
        
        return {'node': node_attribs, 'node_tags': unique_tags}

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
            addtl_tags = []
            
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
                addtl_tags.append(get_additional_shop_tags(value))
            elif key == 'phone':
                way_tags['value'] = update_phone(value)
            elif key == 'Phone':
                key = 'phone'
                way_tags['value'] = update_phone(value)
            elif key == 'phone_1':
                key = 'phone'
                way_tags['value'] = update_phone(value)
            elif key == 'contact:phone':
                way_tags['value'] = update_phone(value)
            elif key == 'phone:emergency':
                way_tags['value'] = update_phone(value)
            elif key == 'fax':
                way_tags['value'] = update_phone(value)
            elif key == 'contact:fax':
                way_tags['value'] = update_phone(value)
            elif key == 'addr:street':
                way_tags['value'] = update_street(value)
                addtl_tags.append(get_additional_street_tags(value))
            elif key == 'addr:place':
                key = get_key(value, key, addr_place_key_mapping)
                way_tags['value'] = clean_w_map(value, addr_place_mapping)
            elif key == 'addr:unit':
                key = change_addr_unit_key(value)
                way_tags['value'] = update_addr_unit(value)
            elif key == 'addr:district':
                way_tags['value'] = update_addr_district(value)  
            elif key == 'building:level':
                key = 'building:levels'
                way_tags['value'] = value
            elif key == 'levels':
                key = 'level'
                way_tags['value'] = value
            elif key == 'addr:level':
                key = 'addr:floor'
                way_tags['value'] = value
            elif key == 'cuisine':
                addtl_tags.extend(update_cuisine(value))
            else:
                way_tags['value'] = value

            way_tags['key'] = key
            
            
            # Additional key and values to append
            for t in addtl_tags:
                for key, val in t.items():
                    addtl_tag = {}
                    addtl_tag['id'] = element.attrib['id']
                    addtl_tag['key'] = key
                    addtl_tag['value'] = val
                    if val is not None:
                        tags.append(addtl_tag)
           
            # Skip any values that are None
            if way_tags.get('value') is None:
                continue
            elif way_tags.get('key') is None or way_tags.get('key') == '':
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

        # Make sure that there are no duplicates in tags
        unique_tags = [i for n, i in enumerate(tags) if i not in tags[n + 1:]]

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': \
                unique_tags}
    
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
            addtl_tags = []
            
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
                addtl_tags.append(get_additional_shop_tags(value))
            elif key == 'phone':
                rel_tags['value'] = update_phone(value)
            elif key == 'Phone':
                key = 'phone'
                rel_tags['value'] = update_phone(value)
            elif key == 'phone_1':
                key = 'phone'
                rel_tags['value'] = update_phone(value)
            elif key == 'contact:phone':
                rel_tags['value'] = update_phone(value)
            elif key == 'phone:emergency':
                rel_tags['value'] = update_phone(value)
            elif key == 'fax':
                rel_tags['value'] = update_phone(value)
            elif key == 'contact:fax':
                rel_tags['value'] = update_phone(value)
            elif key == 'addr:street':
                rel_tags['value'] = update_street(value)
                addtl_tags.append(get_additional_street_tags(value))
            elif key == 'addr:place':
                key = get_key(value, key, addr_place_key_mapping)
                rel_tags['value'] = clean_w_map(value, addr_place_mapping)
            elif key == 'addr:unit':
                key = change_addr_unit_key(value)
                rel_tags['value'] = update_addr_unit(value)
            elif key == 'addr:district':
                rel_tags['value'] = update_addr_district(value)
            elif key == 'building:level':
                key = 'building:levels'
                rel_tags['value'] = value
            elif key == 'levels':
                key = 'level'
                rel_tags['value'] = value
            elif key == 'addr:level':
                key = 'addr:floor'
                rel_tags['value'] = value
            elif key == 'cuisine':
                addtl_tags.extend(update_cuisine(value))
            else:
                rel_tags['value'] = str(value)
            
            rel_tags['key'] = key
            
            # Additional key and values to append
            for t in addtl_tags:
                for key, val in t.items():
                    addtl_tag = {}
                    addtl_tag['id'] = element.attrib['id']
                    addtl_tag['key'] = key
                    addtl_tag['value'] = val
                    if val is not None:
                        tags.append(addtl_tag)
            
            # Skip any values that are None
            if rel_tags.get('value') == None:
                continue
            elif rel_tags.get('key') is None or rel_tags.get('key') == '':
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
        
        # Make sure that there are no duplicates in tags
        unique_tags = [i for n, i in enumerate(tags) if i not in tags[n + 1:]]

        return {'relation': rel_attribs, 'relation_tags': unique_tags, 
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
        print(validator.errors)
        pprint(element)

# Main function
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csvs"""
    
    with open(NODES_PATH, 'w') as nodes_file, \
         open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         open(WAYS_PATH, 'w') as ways_file, \
         open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         open(WAY_TAGS_PATH, 'w') as way_tags_file, \
         open(RELATIONS_PATH, 'w') as relations_file, \
         open(RELATION_TAGS_PATH, 'w') as rel_tags_file, \
         open(RELATION_MEMBERS_PATH, 'w') as rel_members_file:
             
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