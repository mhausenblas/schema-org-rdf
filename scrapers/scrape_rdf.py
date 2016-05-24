import schema_scraper
import sys
import datetime
import schema2rdf

if len(sys.argv) > 2:
    print "Usage: python scrape_rdf.py output.ttl"
    sys.exit()

if len(sys.argv) == 1:
    out = sys.stdout
else:
    out = open(sys.argv[1], 'wb')

# Get ordered list
types_list = schema_scraper.get_all_type_urls().keys();
# Get details for types and properties
types = schema_scraper.get_all_types()
types = schema_scraper.add_supertype_relationships(types)
properties = schema_scraper.collect_properties(types)
types = schema_scraper.remove_property_details(types)
(types, datatypes) = schema_scraper.split_types_datatypes(types)

date = datetime.date.today().isoformat()

print >> sys.stderr, 'Writing Turtle'
schema2rdf.dump_rdf(types_list, types, properties, date, out)
