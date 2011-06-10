""" 
  A processor for Schema.org terms - parsing MD, JSON, CSV, OData, etc. and emitting RDF, JSON, etc. 

  Parsers: for microdata, edsu's awesome MD parser https://github.com/edsu/microdata is used

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-06-09
@status: integrating edsu's MD parser
"""
import StringIO
import urllib2
import uuid
import rdflib
import rdflib_microdata
import microdata

class SchemaOrgProcessor(object):
	def __init__(self):
		self.items = None
		self.item_count = 0
		self.g = None

	###############################################################################
	# primary data interface
	
	def parse_URL(self, doc_url):
		format = self.sniff(doc_url)
		if format == 'microdata':
			print('DETECTED Schema.org terms encoded in microdata ...')
			self.parse_microdata_URL(doc_url)
		elif format == 'csv':
			print('Schema.org in CSV not yet supported ...')
			pass
		else:
			print('Unknown format')
			pass
			
	def sniff(self, doc_url):
		if doc_url.endswith('html'):
			# TODO: need to inspect content, really, to determine if microdata or RDFa
			return 'microdata'
		elif doc_url.endswith('csv'):
			return 'csv'
		else: return None
	
	def parse_microdata_URL(self, doc_url):
		self.g = rdflib.Graph()
		self.g.parse(doc_url, format="microdata")

	def parse_microdata_str(self, html_str):
		self.g = rdflib.Graph()
		b = StringIO.StringIO()
		b.write(html_str)
		self.g.parse(b, format="microdata")
			
	def dump_data(self):
		print('DUMP Schema.org data ...')
		if self.g:
			self.g.bind('schema', 'http://schema.org/', True) # hmm ... has no effect
			print(self.g.serialize()) #format='n3')) ... doesn't work - TODO: ask Ed
		else:
			print('Sorry, nothing to show - use parse_str() or parse_URL() to parse data with Schema.org terms ...')

	###############################################################################	
	# microdata low-level interface
	def items_from_URL(self, doc_url):
		self.items = []
		self.items = microdata.get_items(urllib2.urlopen(doc_url).read())
		self.inspect_items()

	def items_from_str(self, html_str):
		self.items = []
		self.items = microdata.get_items(html_str)
		self.inspect_items()

	def dump_items(self, format='plain'):
		if self.items:
			if format == 'plain': # pure text dump, for example in CLI usage
				print('\n' + '*' * 80)
				print('%s data items found in total:' %self.item_count)
				for it in self.items:
					self.dump_item(it)
			elif format == 'json':
				for it in self.items:
					print(it.json())
		else:
			print('Sorry, nothing to show - use items_from_str() or items_from_URL() to parse microdata ...')
	
	def dump_item(self, item, level='', parent=None, prop=None):
		anonid = uuid.uuid1()
		if parent:
			ith = '%s%s ->\n%sITEM (' %(level, prop, level)
		else:
			ith = 'ITEM ('
			print('-' * 80)
		# the item header (identity and type, if given)
		if item.itemid: ith = ''.join([ith, str(item.itemid)])  
		else: ith = ''.join([ith, 'anonymous::', str(anonid)])
		if item.itemtype: ith = ''.join([ith, ') OF TYPE (', str(item.itemtype), ') {'])  
		else: ith = ''.join([ith, ') {'])
		print(ith)
		for prop, values in item.props.items():
			for val in values:
				if isinstance(val, microdata.Item):
					if item.itemid: parent = str(item.itemid)
					else: parent = str(anonid)
					self.dump_item(val, level=level+ '  ', parent=parent, prop=prop)
				else:
					print(''.join([level, '  ', prop,' = ', str(val)]))
		print(level + '}')

	def inspect_items(self):
		for it in self.items:
			self.inspect_item(it)

	def inspect_item(self, item):
		self.item_count = self.item_count + 1
		for prop, values in item.props.items():
			for val in values:
				if isinstance(val, microdata.Item): self.inspect_item(val)
				else: pass

if __name__ == "__main__":
	md_doc_URI = "test/solar-system.csv"
	mdp = SchemaOrgProcessor()
	mdp.parse_URL(md_doc_URI)
	# mdp.parse_microdata_str("""
	# <div itemscope itemid="http://example.org/event123" itemtype="http://schema.org/Event">
	#   <a itemprop="url" href="nba-miami-philidelphia-game3.html">
	#   NBA Eastern Conference First Round Playoff Tickets:
	#   Miami Heat at Philadelphia 76ers - Game 3 (Home Game 1)
	#   </a>
	# 
	#   <time itemprop="startDate" datetime="2011-04-21T20:00">
	#     Thu, 04/21/11
	#     8:00 p.m.
	#   </time>
	# 
	#   <div itemprop="location" itemscope itemtype="http://schema.org/Place">
	#     <a itemprop="url" href="wells-fargo-center.html">
	#     Wells Fargo Center
	#     </a>
	#     <div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">
	#       <span itemprop="addressLocality">Philadelphia</span>,
	#       <span itemprop="addressRegion">PA</span>
	#     </div>
	#   </div>
	# 
	#   <div itemprop="offers" itemscope itemtype="http://schema.org/AggregateOffer">
	#     Priced from: <span itemprop="lowPrice">$35</span>
	#     <span itemprop="offerCount">1,938</span> tickets left
	#   </div>
	# </div>
	# <div itemscope itemid="http://example.org/event456">
	# </div>
	# <div itemscope itemtype="http://schema.org/Event">
	# </div>
	# <div itemscope>
	# </div>	
	# """)
	mdp.dump_data()