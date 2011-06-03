import urllib
import lxml.html
import lxml.etree
import re
import string

warnings = []

def parse(url):
    root = lxml.html.fromstring(urllib.urlopen(url).read())
    root.make_links_absolute(url)
    return root

def get_all_types(url):
    root = parse(url)
    result = []
    for a in root.cssselect("a[name]"):
        result.append(a.getnext().get('href'))
    return result

def get_inner_html(el):
    result = el.text
    for c in el.getchildren():
        result += lxml.etree.tostring(c)
    return result
    
def get_type_details(url):
    root = parse(url)
    details = {}
    details['url'] = url
    ancestor_links = root.cssselect("h1.page-title a")
    ancestor_links.reverse()
    details['id'] = ancestor_links[0].text_content()
    details['label'] = get_label(details['id'])
    del ancestor_links[0]
    details['ancestors'] = []
    for a in ancestor_links:
        details['ancestors'].append(a.get('href'))
    el = root.cssselect("h1.page-title")[0]
    details['comment'] = el.tail
    details['comment_plain'] = el.tail
    while el.getnext().tag not in ['div', 'h3', 'table']:
        details['comment'] += lxml.etree.tostring(el.getnext())
        details['comment_plain'] += el.getnext().text_content() + el.getnext().tail
        el = el.getnext()
    if details['comment'] == None:
        warnings.append('No comment in type ' + details['id'])
    details['instances'] = []
    details['subtypes'] = []
    details['supertypes'] = []
    for section in root.cssselect("h3"):
        if section.text_content().startswith('Instances'):
            for a in section.getnext().cssselect("li a"):
                details['instances'].append(a.get("href"))
        elif section.text_content().startswith("More specific"):
            for a in section.getnext().cssselect("li a"):
                details['subtypes'].append(a.get("href"))
    if len(details['instances']) == 0:
        del details['instances']
    details['properties'] = []
    group = ''
    for row in root.cssselect("table.definition-table tr"):
        # is this a row introducing a new type?
        cells = row.cssselect("th.supertype-name a")
        if len(cells) > 0:
            group = cells[0].text_content()
            continue
        # skip properties inherited from supertypes
        if group != details['id']:
            continue
        name = row.cssselect("th.prop-nam code")[0].text_content()
        ranges = []
        for a in row.cssselect("td.prop-ect a"):
            ranges.append(a.get('href'))
        if len(ranges) == 0:
            ranges = row.cssselect("td.prop-ect")[0].text_content().split(' or ')
        comment = row.cssselect("td.prop-desc")[0]
        desc = get_inner_html(comment)
        details['properties'].append(
            {'id': name, 'label': get_label(name), 'ranges': ranges, 'comment': desc, 'comment_plain': comment.text_content()})
    return details

def get_label(s):
    s = re.sub('(.)([A-Z][a-z])', '\\1 \\2', s)
    return s[0].upper() + s[1:]
