"""
This rdflib plugin (based on Ed's https://github.com/edsu/rdflib-microdata/) lets you parse CSV
files that use Schema.org column headers into an RDF graph. You shouldn't have to use this module
directly, since it's a plugin. You'll just want to:

>>> import rdflib
>>> import rdflib_schemaorg_csv
>>> g = rdflib.Graph()
>>> g.parse("test.csv", format="schemaorg_csv")
>>> print g.serialize()
"""

import csv
import StringIO
import sys
from rdflib import URIRef, Literal, BNode, Namespace, RDF
from rdflib.plugin import register
from rdflib.parser import Parser


register("schemaorg_csv", Parser, "rdflib_schemaorg_csv", "SchemaOrgCSVParser")

class SchemaOrgCSVParser(Parser):

	def parse(self, source, sink, **kwargs):
		"""
		Pass in a file or file-like object containing CSV with Schema.org
		column headers and populate the sink graph with triples.
		"""
		try:
			rows = csv.reader(source, delimiter=' ', quoting=csv.QUOTE_ALL)
			for row in source:
				self._add_row(row, sink)
		except csv.Error, e:
			sys.exit('%s' %e)

	def _add_row(self, row, sink):
		# the URI to hang our assertions off of
		s = BNode()

		ns = str('http://example.org/')
		# if ns.endswith("#") or ns.endswith("/"):
		# 	ns = Namespace(item.itemtype)
		# else:
		# 	ns = Namespace(ns + "#")

		sink.add((s, RDF.type, str('http://example.org/')))
		p = URIRef('http://schema.org/Property')
		# o = URIRef(row)
		o = Literal(row)
		sink.add((s, p, o))

		return s