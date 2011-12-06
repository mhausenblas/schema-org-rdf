import json
import datetime

def dump_json(datatypes, types, properties, date, out):
    print >> out, json.dumps({'types': types, 'datatypes': datatypes, 'properties': properties, 'valid': date}, sort_keys=True, indent=2)
