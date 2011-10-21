"""
  A processor for Schema.org terms - parsing MD, JSON, CSV, OData, etc. and emitting RDF, JSON, etc.

  Parsers: for microdata, edsu's awesome MD parser https://github.com/edsu/microdata is used

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-06-09
@status: cleaning up and KISSing it
"""
import sys
import getopt
import StringIO
import urllib
import urllib2
import uuid
import rdflib
import rdflib_microdata
import rdflib_schemaorg_csv
import microdata

from rdflib.parser import StringInputSource

class SchemaOrgProcessor(object):
	def __init__(self):
		self.g = None
		self.doc_url = ""

	def parse(self, doc_url, input_format=None):
		self.doc_url = doc_url

		if input_format: # we have a user-supplied input format
			format = input_format
		else: # ... we need to guess the format
			format = self.sniff(doc_url)

		# based on the format information we parse the input:
		if format == 'microdata':
			self.parse_microdata(doc_url)
			return format
		elif format == 'csv':
			self.parse_csv(doc_url)
			return format
		elif format == 'odata':
			# http://code.google.com/p/odata-py/
			return None
		else:
			return None

	def sniff(self, doc_url):
		if doc_url.endswith('html'):
			# TODO: need to inspect content, really, to determine if microdata or RDFa
			return 'microdata'
		elif doc_url.endswith('csv'):
			return 'csv'
		else: return None

	def parse_csv(self, doc_url):
		self.doc_url = doc_url
		self.g = rdflib.Graph()
		self.g.parse(location=doc_url, format="schemaorg_csv", csv_file_URI=self.doc_url)

	def parse_microdata(self, doc_url):
		self.doc_url = doc_url
		self.g = rdflib.Graph()
		self.g.parse(location=doc_url, format="microdata")

	def dump_data(self, format='turtle'):
		if self.g:
			self.g.bind('schema', 'http://schema.org/', True)
			self.g.bind('scsv', 'http://purl.org/NET/schema-org-csv#', True)
			self.g.bind('dcterms', 'http://purl.org/dc/terms/', True)
			return self.g.serialize(format=format)
		else:
			return None

	def get_data(self):
		if self.g:
			return self.g
		else:
			return None

def usage():
	print("Usage: python schema_org_processor.py -d {document URL} ")
	print("Example (translating from microdata): python schema_org_processor.py -d https://raw.github.com/edsu/microdata/master/test-data/example.html")
	print("Example (translating from CSV): python schema_org_processor.py -d https://raw.github.com/mhausenblas/schema-org-rdf/master/tools/schema-gateway/test/solar-system.csv")

if __name__ == "__main__":
	sop = SchemaOrgProcessor()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "data"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				usage()
				sys.exit()
			elif opt in ("-d", "--data"):
				print("PARSING [%s] for Schema.org data ..." %arg)
				doc_url = arg
				sop.parse(doc_url)
				print(sop.dump_data())
				pass
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)