import csv

def dump_types_csv(types, out):
    csv_writer = csv.writer(out)
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

def dump_properties_csv(properties, out):
    csv_writer = csv.writer(out)
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
