# OpenStreetMap Data Wrangling and Case Study
***

The goal of this project was to clean fields of interest using Python and explore the OpenStreetMap data for lower Manhattan and parts of Brooklyn using SQL.

Each individual field has a separate Python script in which the field is audited and cleaning functions and mappings are defined:
* addr_city.py
* addr_country.py
* addr_floor.py
* addr_full.py
* addr_housenumber.py
* addr_place.py
* addr_postcode.py
* addr_state.py
* addr_street.py
* addr_unit.py
* amenity.py
* building.py
* building_material.py
* capacity.py
* cuisine.py
* highway.py
* leisure.py
* phone.py
* roof_material.py
* shop.py

Auditing functions that were used in most of the scripts were defined in auditing.py.  cleaning.py contains two general  cleaning functions and mappings for fields that only need a mapping to be cleaned.  clean_tag_values.py audits the clean tags.  The schema for the database is defined in schema.py.  osm_to_csv.py reads in the OSM map data, cleans it, and writes it to csvs according to the schema.  create_db.py reads the csvs and creates a SQLite database, osm.db.
