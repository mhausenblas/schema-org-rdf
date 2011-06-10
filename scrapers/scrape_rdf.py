import schema_scraper
import string
import sys

def get_prefixed(id):
    if id == 'Text':
        return 'xsd:string'
    if id == 'Date':
        return 'xsd:date'
    if id == 'URL':
        return 'rdfs:Resource'
    if id == 'Boolean':
        return 'xsd:boolean'
    if id == 'Number':
        return 'xsd:decimal'
    if id == 'Float':
        return 'xsd:decimal'
    if id == 'Integer':
        return 'xsd:integer'
    return 'schema:' + id

def turtle_escape(s):
    return s.replace('"', '\\"').encode('utf-8')

# Get ordered list
types_list = schema_scraper.get_all_type_ids()
# Get details for types and properties
types = schema_scraper.get_all_types()
types = schema_scraper.add_supertype_relationships(types)
properties = schema_scraper.collect_properties(types)
types = schema_scraper.remove_property_details(types)
(types, datatypes) = schema_scraper.split_types_datatypes(types)

print >> sys.stderr, 'Writing Turtle'

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

for id in types_list:
    if id not in types: continue        # skip datatypes
    t = types[id]
    print get_prefixed(id) + ' a rdfs:Class;'
    print '    rdfs:label "' + turtle_escape(t['label']) + '"@en;'
    if t['comment_plain'] != None:
        print '    rdfs:comment "' + turtle_escape(t['comment_plain']) + '"@en;'
    for supertype in t['supertypes']:
        print '    rdfs:subClassOf ' + get_prefixed(supertype) + ';'
    print '    rdfs:isDefinedBy <' + t['url'] + '>;'
    print '    .'

prop_ids = properties.keys()
prop_ids.sort()
for id in prop_ids:
    p = properties[id]
    print get_prefixed(p['id']) + ' a rdf:Property;'
    print '    rdfs:label "' + turtle_escape(p['label']) + '"@en;'
    print '    rdfs:comment "' + turtle_escape(p['comment_plain']) + '"@en;'
    if len(p['domains']) == 1:
        print '    rdfs:domain ' + get_prefixed(p['domains'][0]) + ';'
    elif len(p['domains']) > 1:
        l = []
        for d in p['domains']:
            l.append(get_prefixed(d))
        print '    rdfs:domain [ owl:unionOf (' + ' '.join(l) + ') ];'
    if len(p['ranges']) == 1:
        print '    rdfs:range ' + get_prefixed(p['ranges'][0]) + ';'
    elif len(p['ranges']) > 1:
        l = []
        for d in p['ranges']:
            l.append(get_prefixed(d))
        print '    rdfs:range [ owl:unionOf (' + ' '.join(l) + ') ];'
    for d in p['domains']:
        print '    rdfs:isDefinedBy <' + types[d]['url'] + '>;'
    print '    .'
