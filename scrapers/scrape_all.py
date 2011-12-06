import schema_scraper
import sys
import datetime
import schema2rdf
import schema2json
import schema2csv

if len(sys.argv) != 5:
    print "Usage: python scrape_all.py output.ttl output.json classes.csv properties.csv"
    sys.exit()

rdf_file = sys.argv[1]
json_file = sys.argv[2]
csv_class_file = sys.argv[3]
csv_property_file = sys.argv[4]
date = datetime.date.today().isoformat()

print >> sys.stderr, 'Scraping schema.org'

# Get ordered list
types_list = schema_scraper.get_all_type_ids()
# Get details for types and properties
types = schema_scraper.get_all_types()
types = schema_scraper.add_supertype_relationships(types)
properties = schema_scraper.collect_properties(types)
types = schema_scraper.remove_property_details(types)
(types, datatypes) = schema_scraper.split_types_datatypes(types)

print >> sys.stderr, 'Writing Turtle to ' + rdf_file
schema2rdf.dump_rdf(types_list, types, properties, date, open(rdf_file, 'wb'))

print >> sys.stderr, 'Writing JSON to ' + json_file
schema2json.dump_json(datatypes, types, properties, date, open(json_file, 'wb'))

print >> sys.stderr, 'Writing classes to ' + csv_class_file
schema2csv.dump_types_csv(types, open(csv_class_file, 'wb'))

print >> sys.stderr, 'Writing properties to ' + csv_property_file
schema2csv.dump_properties_csv(properties, open(csv_property_file, 'wb'))
