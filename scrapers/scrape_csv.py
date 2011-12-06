import schema_scraper
import sys
import schema2csv

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
schema2csv.dump_types_csv(types, open(class_file, 'wb'))

print >> sys.stderr, 'Writing properties to ' + property_file
schema2csv.dump_properties_csv(properties, open(property_file, 'wb'))
