import urllib
import lxml.html
import lxml.etree
import re
import sys
import time

base_url = 'http://schema.org/'
full_docs_url = 'http://schema.org/docs/full.html'

class AppURLopener(urllib.URLopener):
    version = "SchemaScraper/1.1 (http://schema.rdfs.org/)"
urllib._urlopener = AppURLopener()

def get_all_types():
    ids = get_all_type_ids()
    types = {}
    for id in ids:
#        print >> sys.stderr, 'Parsing page for ' + id
        types[id] = get_type_details(base_url + id)
        time.sleep(1)
    return types

def parse(url):
    root = lxml.html.fromstring(urllib.urlopen(url).read())
    root.make_links_absolute(url)
    return root

def get_all_type_ids():
    root = parse(full_docs_url)
    types = []
    for a in root.cssselect("#thing_tree a[href], #datatype_tree a[href]"):
        id = a.text_content()
        if id[-1] == '+': continue
        types.append(id)
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
    ancestor_links = root.cssselect(".breadcrumbs a")
    id = ancestor_links[-1].text_content().strip()
    print id
    type['id'] = id
    del ancestor_links[-1]
    type['label'] = get_label(id)
    type['ancestors'] = []
    for a in ancestor_links:
        type['ancestors'].append(a.text_content().strip())
    el = root.cssselect("div[property='rdfs:comment']")[0]
    type['comment'] = get_inner_html(el)
    type['comment_plain'] = el.text_content().strip()
    type['instances'] = []
    type['subtypes'] = []

    row = root.cssselect("#mainContent > ul:last-of-type")
    if len(row) > 0:
        for a in row[0].cssselect("li a"):
            type['subtypes'].append(a.text_content().strip())

    for section in root.cssselect("table.definition-table:nth-of-type(2) tr"):
        if len(row) > 0:
            for a in section.cssselect("code a"):
                type['instances'].append(a.text_content().strip())

    if len(type['instances']) == 0:
        del type['instances']
    type['properties'] = []
    type['specific_properties'] = []
    type['property_details'] = []
    group = ''

    for row in root.cssselect("table.definition-table:nth-of-type(1) tr"):
        # is this a row introducing a new type?
        cells = row.cssselect("th.supertype-name a")
        if len(cells) > 0:
            group = cells[0].text_content().strip()
            continue
        if group == '': continue

        if len(row.cssselect("th.prop-nam code")) == 0:
            continue

        name = row.cssselect("th.prop-nam code")[0].text_content().strip()
        comment = row.cssselect("td.prop-desc")[0]
        type['properties'].append(name)
        if group != id: continue
        type['specific_properties'].append(name)
        type['property_details'].append({
                'id': name,
                'label': get_label(name),
                'domains': [id],
                'ranges': re.sub('\s+', ' ', row.cssselect("td.prop-ect")[0].text_content()).replace(u'\xa0', '').strip().encode('utf-8').split(' or '),
                'comment': get_inner_html(comment),
                'comment_plain': comment.text_content().strip(),
                'url': base_url + id
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
            if subtype in types:
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
