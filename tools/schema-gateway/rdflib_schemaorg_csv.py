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
	NAMESPACES = {	
		'schema' : Namespace('http://schema.org/'),
		'scsv' : Namespace('http://purl.org/NET/schema-org-csv#'),
		'dcterms' : Namespace('http://purl.org/dc/terms/')
	}
	
	def parse(self, source, sink, **kwargs):
		"""
		Pass in a file or file-like object containing CSV with Schema.org
		column headers and populate the sink graph with triples.
		"""
		row_num = 1
		fURI = kwargs.get("csv_file_URI", "")
		self._add_table(fURI, sink)
		try:
			f = source.getByteStream()
			rows = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
			for row in rows:
				if row_num == 1:
					columns = self._add_header(fURI, row, row_num, sink)
				else:
					self._add_row(fURI, columns, row, row_num, sink)
				row_num = row_num + 1
			f.close()
		except csv.Error, e:
			sys.exit('%s' %e)

	def _add_table(self, fURI, sink):
		t = URIRef(fURI + '#table')
		sink.add((t, RDF.type, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['Table'])))
		sink.add((t, SchemaOrgCSVParser.NAMESPACES['dcterms']['source'], URIRef(fURI)))
		sink.add((t, SchemaOrgCSVParser.NAMESPACES['dcterms']['title'], Literal(fURI.split('/')[-1])))

	def _add_header(self, fURI, row, row_num, sink):
		t = URIRef(fURI + '#table')
		r = URIRef(fURI + '#row:' + str(row_num))
		# row-level:
		sink.add((t, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['row']), r))
		sink.add((r, RDF.type, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['HeaderRow'])))
		sink.add((r, SchemaOrgCSVParser.NAMESPACES['dcterms']['title'], Literal('header')))
		# cell-level:
		col_num = 1
		columns = []
		for cell in row:
			c = URIRef(fURI + '#row:' + str(row_num) + ',' + 'col:' + str(col_num))
			sink.add((r, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['cell']), c))
			sink.add((c, SchemaOrgCSVParser.NAMESPACES['dcterms']['title'], Literal(cell)))
			columns.append(self._lookup_schemaorg_term(cell)) 
			col_num = col_num + 1
		return columns

	def _add_row(self, fURI, columns, row, row_num, sink):
		t = URIRef(fURI + '#table')
		r = URIRef(fURI + '#row:' + str(row_num))
		# row-level:
		sink.add((t, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['row']), r))
		sink.add((r, RDF.type, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['Row'])))
		sink.add((r, SchemaOrgCSVParser.NAMESPACES['dcterms']['title'], Literal('row ' + str(row_num))))
		# cell-level:
		col_num = 1
		for cell in row:
			c = URIRef(fURI + '#row:' + str(row_num) + ',' + 'col:' + str(col_num))
			sink.add((r, URIRef(SchemaOrgCSVParser.NAMESPACES['scsv']['cell']), c))
			sink.add((c, RDF.type, URIRef(columns[col_num - 1])))
			if cell.startswith('http://'):
				sink.add((c, RDF.value, URIRef(cell)))
			else:
				sink.add((c, RDF.value, Literal(cell)))
			col_num = col_num + 1
		return r
		
	def _lookup_schemaorg_term(self, cell):
			return 'http://schema.org/' + cell # TODO: look up cell value in http://schema.rdfs.org/all-classes.csv