import urllib
import lxml.html
import lxml.etree
import re
import sys

base_url = 'http://schema.org/'
full_docs_url = 'http://schema.org/docs/full.html'

class AppURLopener(urllib.URLopener):
    version = "SchemaScraper/1.0 (http://schema.rdfs.org/)"
urllib._urlopener = AppURLopener()

def get_all_types():
    ids = get_all_type_ids()
    types = {}
    for id in ids:
#        print >> sys.stderr, 'Parsing page for ' + id
        types[id] = get_type_details(base_url + id)
    return types

def parse(url):
    root = lxml.html.fromstring(urllib.urlopen(url).read())
    root.make_links_absolute(url)
    return root

def get_all_type_ids():
    root = parse(full_docs_url)
    types = []
    for a in root.cssselect("a[name]"):
        types.append(a.getnext().text_content())
    return types

def get_inner_html(el):
    result = el.text
    for c in el.getchildren():
        result += lxml.etree.tostring(c)
    return result

def get_type_details(url):
    root = parse(url)
    type = {}
    type['url'] = url
    ancestor_links = root.cssselect("h1.page-title a")
    id = ancestor_links[-1].text_content()
    type['id'] = id
    del ancestor_links[-1]
    type['label'] = get_label(id)
    type['ancestors'] = []
    for a in ancestor_links:
        type['ancestors'].append(a.text_content())
    el = root.cssselect("h1.page-title")[0]
    type['comment'] = el.tail
    type['comment_plain'] = el.tail
    while el.getnext().tag not in ['div', 'h3', 'table']:
        type['comment'] += lxml.etree.tostring(el.getnext())
        type['comment_plain'] += el.getnext().text_content() + el.getnext().tail
        el = el.getnext()
    if type['comment'] == None:
        print >> sys.stderr, 'WARNING: No comment in type ' + id
    type['instances'] = []
    type['subtypes'] = []
    for section in root.cssselect("h3"):
        if section.text_content().startswith('Instances'):
            for a in section.getnext().cssselect("li a"):
                type['instances'].append(a.text_content())
        elif section.text_content().startswith("More specific"):
            for a in section.getnext().cssselect("li a"):
                type['subtypes'].append(a.text_content())
    if len(type['instances']) == 0:
        del type['instances']
    type['properties'] = []
    type['specific_properties'] = []
    type['property_details'] = []
    group = ''
    for row in root.cssselect("table.definition-table tr"):
        # is this a row introducing a new type?
        cells = row.cssselect("th.supertype-name a")
        if len(cells) > 0:
            group = cells[0].text_content()
            continue
        if group == '': continue
        name = row.cssselect("th.prop-nam code")[0].text_content()
        comment = row.cssselect("td.prop-desc")[0]
        type['properties'].append(name)
        if group != id: continue
        type['specific_properties'].append(name)
        type['property_details'].append({
                'id': name,
                'label': get_label(name),
                'domains': [id],
                'ranges': row.cssselect("td.prop-ect")[0].text_content().split(' or '),
                'comment': get_inner_html(comment),
                'comment_plain': comment.text_content()
        })
    return type

def get_label(s):
    # MusicEvent => Music Event
    s = re.sub('(?<=.)([A-Z][a-z])', ' \\1', s)
    # ContentURL => Content URL
    s = re.sub('([a-z])([A-Z])', '\\1 \\2', s)
    # description => Description
    s = s[0].upper() + s[1:];
    # Is Part Of => Is Part of
    for word in ['For', 'Of', 'Or', 'By', 'In', 'To']:
        s = re.sub(' ' + word + '($| )', ' ' + word.lower() + '\\1', s)
    # Url => URL
    for word in ['Url', 'Isbn']:
        if s == word: s = word.upper()
    return s

def add_supertype_relationships(types):
    for id in types: types[id]['supertypes'] = []
    for id in types:
        for subtype in types[id]['subtypes']:
            types[subtype]['supertypes'].append(id)
    return types

def collect_properties(types):
    properties = {}
    for tid in types:
        for property in types[tid]['property_details']:
            pid = property['id']
            for rid in property['ranges']:
                if rid in types: continue
                print >> sys.stderr, 'WARNING: Undefined expected type ' + rid + ' for property ' + pid + ' of type ' + tid
            if pid in properties:
                properties[pid]['ranges'] = list(set(properties[pid]['ranges'] + property['ranges']))
                properties[pid]['domains'] = list(set(properties[pid]['domains'] + property['domains']))
            else:
                properties[pid] = property
    return properties

def remove_property_details(types):
    for id in types:
        del types[id]['property_details']
    return types

def split_types_datatypes(types):
    t = {}
    dt = {}
    for id in types:
        if id == 'DataType' or 'DataType' in types[id]['ancestors']:
            dt[id] = types[id]
        else:
            t[id] = types[id]
    return (t, dt)
