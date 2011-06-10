import schema_scraper
import sys
import csv

if len(sys.argv) != 3:
    print "Usage: python scrape_csv.py classes.csv properties.csv"
    sys.exit()

class_file = sys.argv[1]
property_file = sys.argv[2]

types = schema_scraper.get_all_types()
types = schema_scraper.add_supertype_relationships(types)
properties = schema_scraper.collect_properties(types)
types = schema_scraper.remove_property_details(types)
(types, datatypes) = schema_scraper.split_types_datatypes(types)

print >> sys.stderr, 'Writing classes to ' + class_file
csv_writer = csv.writer(open(class_file, 'wb'))
csv_writer.writerow(['id', 'label', 'comment', 'ancestors', 'supertypes', 'subtypes', 'properties'])
for id in types:
    type = types[id]
    if type['comment'] == None: type['comment'] = ''
    row = []
    row.append(id)
    row.append(type['label'].encode('utf-8'))
    row.append(type['comment'].encode('utf-8'))
    row.append(' '.join(type['ancestors']))
    row.append(' '.join(type['supertypes']))
    row.append(' '.join(type['subtypes']))
    row.append(' '.join(type['specific_properties']))
    csv_writer.writerow(row)

print >> sys.stderr, 'Writing properties to ' + property_file
csv_writer = csv.writer(open(property_file, 'wb'))
csv_writer.writerow(['id', 'label', 'comment', 'domains', 'ranges'])
for id in properties:
    property = properties[id]
    if property['comment'] == None: property['comment'] = ''
    row = []
    row.append(id)
    row.append(property['label'].encode('utf-8'))
    row.append(property['comment'].encode('utf-8'))
    row.append(' '.join(property['domains']))
    row.append(' '.join(property['ranges']))
    csv_writer.writerow(row)
