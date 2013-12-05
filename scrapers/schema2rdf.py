from rdflib import Literal


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


def turtle_literal(string):
    return Literal(string, lang='en').n3().encode('utf-8')


def dump_rdf(types_list, types, properties, date, out):

    print >> out, """@prefix schema: <http://schema.org/>.
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
    dct:hasFormat [
        dct:hasPart <http://schema.rdfs.org/all-classes.csv>;
        dct:hasPart <http://schema.rdfs.org/all-properties.csv>;
    ];
    dct:source <http://schema.org/>;
    dct:license <http://schema.org/docs/terms.html>;"""
    print >> out, '    dct:valid "' + date + '"^^xsd:date;'
    print >> out, '    .\n'

    for id in types_list:
        if id not in types: continue        # skip datatypes
        t = types[id]
        print >> out, get_prefixed(id) + ' a rdfs:Class;'
        print >> out, '    rdfs:label %s;' % turtle_literal(t['label'])
        if t['comment_plain'] is not None:
            print >> out, '    rdfs:comment %s;' % turtle_literal(t['comment_plain'])
        for supertype in t['supertypes']:
            print >> out, '    rdfs:subClassOf ' + get_prefixed(supertype) + ';'
        print >> out, '    rdfs:isDefinedBy <' + t['url'] + '>;'
        print >> out, '    .'

    prop_ids = properties.keys()
    prop_ids.sort()
    for id in prop_ids:
        p = properties[id]
        print >> out, get_prefixed(p['id']) + ' a rdf:Property;'
        print >> out, '    rdfs:label %s;' % turtle_literal(p['label'])
        print >> out, '    rdfs:comment %s;' % turtle_literal(p['comment_plain'])
        if len(p['domains']) == 1:
            print >> out, '    rdfs:domain ' + get_prefixed(p['domains'][0]) + ';'
        elif len(p['domains']) > 1:
            l = []
            for d in p['domains']:
                l.append(get_prefixed(d))
            print >> out, '    rdfs:domain [ a owl:Class; owl:unionOf (' + ' '.join(l) + ') ];'
        if len(p['ranges']) == 1:
            print >> out, '    rdfs:range ' + get_prefixed(p['ranges'][0]) + ';'
        elif len(p['ranges']) > 1:
            l = []
            for d in p['ranges']:
                l.append(get_prefixed(d))
            print >> out, '    rdfs:range [ a owl:Class; owl:unionOf (' + ' '.join(l) + ') ];'
        for d in p['domains']:
            print >> out, '    rdfs:isDefinedBy <' + types[d]['url'] + '>;'
        print >> out, '    .'
