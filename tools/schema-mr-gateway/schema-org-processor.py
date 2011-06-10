""" 
  Microdata processor - parsing MD and emitting RDF, JSON, etc. 

  Using edsu's awesome MD parser https://github.com/edsu/microdata

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-06-09
@status: initial draft
"""
import urllib2
import microdata

class MicrodataProcessor(object):
	def __init__(self):
		self.items = []
		self.item_count = 0

	def from_URL(self, doc_url):
		self.items = microdata.get_items(urllib2.urlopen(doc_url).read())
		slef.inspect_items()
		
	def from_str(self, html_str):
		self.items = microdata.get_items(html_str)
		self.inspect_items()

	def dump_items(self, format='plain'):
		if format == 'plain': # pure text dump, for example in CLI usage
			print('%s data items found in total:' %self.item_count)
			for it in self.items:
				self.dump_item(it)
				print('\n')
		elif format == 'json':
			for it in self.items:
				print(it.json())
	
	def dump_item(self, item):
		ith = 'ITEM ('
		print('-' * 80)
		# the item header (identity and type, if given)
		if item.itemid: ith = ''.join([ith, item.itemid])  
		else: ith = ''.join([ith, 'anonymous'])
		if item.itemtype: ith = ''.join([ith, ') of type (', item.itemtype, ')'])  
		else: ith = ''.join([ith, ') without type'])
		print(ith)
		for prop, values in item.props.items():
			for val in values:
				if isinstance(val, microdata.Item): self.dump_item(val)
				else:
					print(' = '.join([prop, str(val)]))

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
	md_doc_URI = "https://raw.github.com/edsu/microdata/master/test-data/example.html"
	mdp = MicrodataProcessor()
	# mdp.from_URL(md_doc_URI)
	mdp.from_str("""
	<div itemscope itemid="http://example.org/event123" itemtype="http://schema.org/Event">
	  <a itemprop="url" href="nba-miami-philidelphia-game3.html">
	  NBA Eastern Conference First Round Playoff Tickets:
	  Miami Heat at Philadelphia 76ers - Game 3 (Home Game 1)
	  </a>
	
	  <time itemprop="startDate" datetime="2011-04-21T20:00">
	    Thu, 04/21/11
	    8:00 p.m.
	  </time>
	
	  <div itemprop="location" itemscope itemtype="http://schema.org/Place">
	    <a itemprop="url" href="wells-fargo-center.html">
	    Wells Fargo Center
	    </a>
	    <div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">
	      <span itemprop="addressLocality">Philadelphia</span>,
	      <span itemprop="addressRegion">PA</span>
	    </div>
	  </div>
	
	  <div itemprop="offers" itemscope itemtype="http://schema.org/AggregateOffer">
	    Priced from: <span itemprop="lowPrice">$35</span>
	    <span itemprop="offerCount">1,938</span> tickets left
	  </div>
	</div>
	<div itemscope itemid="http://example.org/event456">
	</div>
	<div itemscope itemtype="http://schema.org/Event">
	</div>
	<div itemscope>
	</div>	
	""")
	mdp.dump_items()