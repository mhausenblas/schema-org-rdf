import schema_scraper
import sys
import datetime
import schema2json

if len(sys.argv) > 2:
    print "Usage: python scrape_json.py output.json"
    sys.exit()

if len(sys.argv) == 1:
    out = sys.stdout
else:
    out = open(sys.argv[1], 'wb')

types = schema_scraper.get_all_types()
types = schema_scraper.add_supertype_relationships(types)
properties = schema_scraper.collect_properties(types)
types = schema_scraper.remove_property_details(types)
(types, datatypes) = schema_scraper.split_types_datatypes(types)

date = datetime.date.today().isoformat()

print >> sys.stderr, 'Writing JSON'
schema2json.dump_json(datatypes, types, properties, date, out)
