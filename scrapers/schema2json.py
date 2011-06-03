import urllib
import lxml.html
import lxml.etree
import re
import string
import schemaparse

base_url = 'http://schema.org/'

def remove_base(l):
    global base_url
    for i in range(0, len(l)):
        if l[i].startswith(base_url):
            l[i] = l[i][len(base_url):]

datatype_url = 'http://schema.org/DataType'
type_urls = schemaparse.get_all_types("http://schema.org/docs/full.html")
type_ids = []
types = {}
types_by_url = {}
properties = {}
for url in type_urls:
    type = schemaparse.get_type_details(url)
    for property in type['properties']:
        for xrange in property['ranges']:
            if xrange in type_urls or not xrange.startswith(base_url): continue
            property['ranges'].remove(xrange)
            schemaparse.warnings.append('Property ' + property['id'] + ' in type ' + type['id'] + ' defines invalid type ' + xrange + ' as range')
        if property['id'] not in properties:
            property['domains'] = [type['url']]
            property['url'] = base_url + property['id']
            properties[property['id']] = property
        else:
            properties[property['id']]['ranges'] = list(set(properties[property['id']]['ranges'] + property['ranges']))
            properties[property['id']]['domains'].append(type['url'])
    del type['properties']
    # Skip datatypes
#    if type['url'] == datatype_url or datatype_url in type['ancestors']:
#        continue
    types[type['id']] = type
    types_by_url[type['url']] = type
    type_ids.append(type['id'])

for id in type_ids:
    remove_base(types[id]['ancestors'])
    remove_base(types[id]['subtypes'])
    remove_base(types[id]['supertypes'])
    for t in types[id]['subtypes']:
        if t in types_by_url:
            types_by_url[t]['supertypes'].append(types[id]['url'])

for id in properties.keys():
    remove_base(properties[id]['domains'])
    remove_base(properties[id]['ranges'])

import json

print json.dumps({'types': types, 'properties': properties}, sort_keys=True, indent=2)
