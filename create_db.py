#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:16:37 2017

@author: Jackie
"""

import sqlite3
import csv
from pprint import pprint

sqlite_file = 'osm.db'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

#%% Create Node table, read in csv and load data into the table 
cur.execute('''
            CREATE TABLE Node (
            id INT PRIMARY KEY NOT NULL,
            lat REAL,
            lon REAL,
            user TEXT,
            uid INT,
            version TEXT,
            changeset INT,
            timestamp DATETIME)
            ''')
conn.commit()

with open('nodes.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'],
              i['changeset'], i['timestamp']) for i in dr]

cur.executemany('''
                INSERT INTO Node(id, lat, lon, user, uid, version,
                changeset, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM Node
            LIMIT 10
            ''')
all_rows = cur.fetchall()
pprint(all_rows)

#%% Create NodeTag table, read in csv and load data into the table 

cur.execute('''
            CREATE TABLE NodeTag (
            id INT,
            key TEXT,
            value TEXT,
            FOREIGN KEY(id) REFERENCES Node(id)
            CONSTRAINT PK_NodeTag PRIMARY KEY (id, key, value))
            ''')
conn.commit()

with open('nodes_tags.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], i['value']) for i in dr]

cur.executemany('INSERT INTO NodeTag(id, key, value) VALUES (?, ?, ?);', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM NodeTag
            LIMIT 20
            ''')
all_rows = cur.fetchall()

pprint(all_rows)

#%% Create Way table, read in csv and load data into the table 
cur.execute('''
            CREATE TABLE Way (
            id INT PRIMARY KEY NOT NULL,
            user TEXT,
            uid INT,
            version TEXT,
            changeset INT,
            timestamp DATETIME)
            ''')
conn.commit()

with open('ways.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'],
              i['timestamp']) for i in dr]

cur.executemany('''
                INSERT INTO Way(id, user, uid, version, changeset, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM Way
            LIMIT 10
            ''')
all_rows = cur.fetchall()
pprint(all_rows)

#%% Create WayNode table, read in csv and load data into the table 

cur.execute('''
            CREATE TABLE WayNode (
            id INT,
            node_id INT,
            position INT,
            FOREIGN KEY(id) REFERENCES Way(id)
            CONSTRAINT PK_WayNode PRIMARY KEY (id, node_id, position))
            ''')
conn.commit()

with open('ways_nodes.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany('''
                INSERT INTO WayNode(id, node_id, position) 
                VALUES (?, ?, ?)
                ''', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM WayNode
            LIMIT 20
            ''')
all_rows = cur.fetchall()

pprint(all_rows)

#%% Create WayTag table, read in csv and load data into the table 

cur.execute('''
            CREATE TABLE WayTag (
            id INT,
            key TEXT,
            value TEXT,
            FOREIGN KEY(id) REFERENCES Way(id)
            CONSTRAINT PK_WayTag PRIMARY KEY (id, key, value))
            ''')
conn.commit()

with open('ways_tags.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], i['value']) for i in dr]

cur.executemany('INSERT INTO WayTag(id, key, value) VALUES (?, ?, ?);', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM WayTag
            LIMIT 20
            ''')
all_rows = cur.fetchall()

pprint(all_rows)

#%% Create Relation table, read in csv and load data into the table 
cur.execute('''
            CREATE TABLE Relation (
            id INT PRIMARY KEY NOT NULL,
            user TEXT,
            uid INT,
            version TEXT,
            changeset INT,
            timestamp DATETIME)
            ''')
conn.commit()

with open('relations.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'],
              i['timestamp']) for i in dr]

cur.executemany('''
                INSERT INTO Relation(id, user, uid, version, changeset,
                timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM Relation
            LIMIT 10
            ''')
all_rows = cur.fetchall()
pprint(all_rows)

#%% Create RelationTag table, read in csv and load data into the table 

cur.execute('''
            CREATE TABLE RelationTag (
            id INT,
            key TEXT,
            value TEXT,
            FOREIGN KEY(id) REFERENCES Relation(id)
            CONSTRAINT PK_RelationTag PRIMARY KEY (id, key, value))
            ''')
conn.commit()

with open('relations_tags.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], i['value']) for i in dr]

cur.executemany('INSERT INTO RelationTag(id, key, value) VALUES (?, ?, ?);'
                , to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM RelationTag
            LIMIT 20
            ''')
all_rows = cur.fetchall()

pprint(all_rows)

#%% Create RelationMember table, read in csv and load data into the table 

cur.execute('''
            CREATE TABLE RelationMember (
            id INT,
            type TEXT,
            node_id INT,
            role TEXT,
            position INT,
            FOREIGN KEY(id) REFERENCES Way(id)
            CONSTRAINT PK_RelationMember PRIMARY KEY
                (id, type, node_id, role, position))
            ''')
conn.commit()

with open('relations_members.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['type'], i['node_id'], i['role'],
              i['position']) for i in dr]

cur.executemany('''
                INSERT INTO RelationMember(id, type, node_id, role, position) 
                VALUES (?, ?, ?, ?, ?)
                ''', to_db)
conn.commit()

cur.execute('''
            SELECT *
            FROM RelationMember
            LIMIT 20
            ''')
all_rows = cur.fetchall()

pprint(all_rows)

#%%
conn.close()