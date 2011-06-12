""" 
  A pretty printer for microdata content.

  Parsers: for microdata, edsu's awesome MD parser https://github.com/edsu/microdata is used

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-06-11
@status: initial
"""
import sys
import getopt
import StringIO
import urllib
import urllib2
import uuid
import microdata


class MicrodataPrettyPrinter(object):
	def __init__(self):
		self.items = None
		self.item_count = 0

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
				obuf = ''.join(['\n', '*' * 80, '\n'])
				obuf = ''.join([obuf, '%s data items found in total:' %self.item_count, '\n'])
				for it in self.items:
					obuf = ''.join([obuf, self.dump_item(it), '\n'])
				return obuf
			elif format == 'json': # JSON dump
				for it in self.items:
					return it.json()
	
	def dump_item(self, item, level='', parent=None, prop=None):
		obuf = ''
		anonid = uuid.uuid1()
		if parent:
			ith = '%s%s ->\n%sITEM (' %(level, prop, level)
		else:
			ith = 'ITEM ('
			obuf = ''.join([obuf, '-' * 80, '\n'])
		# the item header (identity and type, if given)
		if item.itemid: ith = ''.join([ith, str(item.itemid)])  
		else: ith = ''.join([ith, 'anonymous::', str(anonid)])
		if item.itemtype: ith = ''.join([ith, ') OF TYPE (', str(item.itemtype), ') {'])  
		else: ith = ''.join([ith, ') {'])
		obuf = ''.join([obuf, ith, '\n'])
		for prop, values in item.props.items():
			for val in values:
				if isinstance(val, microdata.Item):
					if item.itemid: parent = str(item.itemid)
					else: parent = str(anonid)
					obuf = ''.join([obuf, self.dump_item(val, level=level+ '  ', parent=parent, prop=prop), '\n'])
				else:
					obuf = ''.join([obuf, ''.join([level, '  ', prop,' = ', str(val)]), '\n'])
		obuf = ''.join([obuf, level, '}', '\n'])
		return obuf

	def inspect_items(self):
		for it in self.items:
			self.inspect_item(it)

	def inspect_item(self, item):
		self.item_count = self.item_count + 1
		for prop, values in item.props.items():
			for val in values:
				if isinstance(val, microdata.Item): self.inspect_item(val)
				else: pass

def usage():
	print("Usage: python microdata_pp.py -i {HTML document URL} ")
	print("Example: python microdata_pp.py -i https://raw.github.com/edsu/microdata/master/test-data/example.html")
	

if __name__ == "__main__":
	mdp = MicrodataPrettyPrinter()
		
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "items"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				usage()
				sys.exit()
			elif opt in ("-i", "--items"):
				print("PARSING [%s] for Schema.org items ..." %arg)
				md_doc_URI = arg
				mdp.items_from_URL(md_doc_URI)
				print(mdp.dump_items())
				pass
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)