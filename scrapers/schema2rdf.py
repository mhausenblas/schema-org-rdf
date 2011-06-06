import urllib
import lxml.html
import lxml.etree
import re
import string
import schemaparse

def get_prefixed(url):
    if url == 'Text':
        return 'xsd:string'
    if url == 'Date':
        return 'xsd:date'
    if url == 'URL':
        return 'rdfs:Resource'
    if url == 'Boolean':
        return 'xsd:boolean'
    if url == 'Number':
        return 'xsd:decimal'
    if url == 'Float':
        return 'xsd:decimal'
    if url == 'Integer':
        return 'xsd:integer'
    if url == 'Duration':
        return 'xsd:duration'
    if url.startswith(base_url):
        return 'schema:' + url[len(base_url):]
    raise Exception(url)

def turtle_escape(s):
    return s.replace('"', '\\"').encode('utf-8')

#print get_type_details("http://schema.org/Thing")

base_url = 'http://schema.org/'
datatype_url = 'http://schema.org/DataType'
type_urls = schemaparse.get_all_types("http://schema.org/docs/full.html")
type_ids = []
types = {}
types_by_url = {}
properties = {}
for url in type_urls:
    type = schemaparse.get_type_details(url)
    for property in type['properties']:
        for range in property['ranges']:
            if range in type_urls or not range.startswith(base_url): continue
            property['ranges'].remove(range)
            schemaparse.warnings.append('Property ' + property['id'] + ' in type ' + type['id'] + ' defines invalid type ' + range + ' as range')
        if property['id'] not in properties:
            property['domains'] = [type['url']]
            property['url'] = base_url + property['id']
            properties[property['id']] = property
        else:
            properties[property['id']]['ranges'] = list(set(properties[property['id']]['ranges'] + property['ranges']))
            properties[property['id']]['domains'].append(type['url'])
    del type['properties']
    # Skip datatypes
    if type['url'] == datatype_url or datatype_url in type['ancestors']:
        continue
    types[type['id']] = type
    types_by_url[type['url']] = type
    type_ids.append(type['id'])

for id in type_ids:
    for t in types[id]['subtypes']:
        if t in types_by_url:
            types_by_url[t]['supertypes'].append(types[id]['url'])

print """@prefix schema: <http://schema.org/>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix dct: <http://purl.org/dc/terms/>.

<http://schema.rdfs.org/all> a owl:Ontology;
    dct:title "The schema.org terms in RDFS+OWL"@en;
    dct:description "This is a conversion of the terms defined at schema.org to RDFS and OWL."@en;
    foaf:page <http://schema.rdfs.org/>;
    rdfs:seeAlso <http://schema.org/>;
    rdfs:seeAlso <http://github.com/mhausenblas/schema-org-rdf>;
    dct:hasFormat <http://schema.rdfs.org/all.ttl>;
    dct:hasFormat <http://schema.rdfs.org/all.rdf>;
    dct:hasFormat <http://schema.rdfs.org/all.nt>;
    dct:hasFormat <http://schema.rdfs.org/all.json>;
    .
"""

for id in type_ids:
    t = types[id]
    print get_prefixed(t['url']) + ' a rdfs:Class;'
    print '    rdfs:label "' + turtle_escape(t['label']) + '"@en;'
    if t['comment_plain'] != None:
        print '    rdfs:comment "' + turtle_escape(t['comment_plain']) + '"@en;'
    for supertype in types[id]['supertypes']:
        print '    rdfs:subClassOf ' + get_prefixed(supertype) + ';'
    print '    rdfs:isDefinedBy <' + t['url'] + '>;'
    print '    .'

prop_ids = properties.keys()
prop_ids.sort()
for id in prop_ids:
    p = properties[id]
    print get_prefixed(p['url']) + ' a rdf:Property;'
    print '    rdfs:label "' + turtle_escape(p['label']) + '"@en;'
    print '    rdfs:comment "' + turtle_escape(p['comment_plain']) + '"@en;'
    if len(p['domains']) == 1:
        print '    rdfs:domain ' + get_prefixed(p['domains'][0]) + ';'
    elif len(p['domains']) > 1:
        l = []
        for d in p['domains']:
            l.append(get_prefixed(d))
        print '    rdfs:domain [ owl:unionOf (' + string.join(l, ' ') + ') ];'
    if len(p['ranges']) == 1:
        print '    rdfs:range ' + get_prefixed(p['ranges'][0]) + ';'
    elif len(p['ranges']) > 1:
        l = []
        for d in p['ranges']:
            l.append(get_prefixed(d))
        print '    rdfs:range [ owl:unionOf (' + string.join(l, ' ') + ') ];'
    print '    rdfs:isDefinedBy <' + p['url'] + '>;'
    print '    .'

print ''
if len(schemaparse.warnings) > 0:
    print '# Conversion warnings:'
for w in schemaparse.warnings:
    print '#     ' + w
