import schema_scraper
import json
import sys

types = schema_scraper.get_all_types()
types = schema_scraper.add_supertype_relationships(types)
properties = schema_scraper.collect_properties(types)
types = schema_scraper.remove_property_details(types)
(types, datatypes) = schema_scraper.split_types_datatypes(types)

print >> sys.stderr, 'Writing JSON'
print json.dumps({'types': types, 'datatypes': datatypes, 'properties': properties}, sort_keys=True, indent=2)
