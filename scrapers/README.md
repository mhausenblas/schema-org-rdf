Ugly, ugly screenscraping business for getting RDF and JSON out of http://schema.org/

Run:
   python schema2rdf.py > all.ttl
   python schema2json.py > all.json
   any23 -f ntriples all.ttl > all.nt
   any23 -f rdfxml all.ttl > all.rdf
