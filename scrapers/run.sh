python schema2rdf.py > all.ttl
any23 -f ntriples all.ttl > all.nt
any23 -f rdfxml all.ttl > all.rdf
python schema2json.py > all.json
