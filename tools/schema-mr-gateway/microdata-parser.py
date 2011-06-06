"""HTML5 microdata parser for python 2.x/3.x

- it requires lxml
- microdata specification: http://dev.w3.org/html5/md/

based on a Gist: https://gist.github.com/577116
"""
try: from urllib.parse import urljoin
except: from urlparse import urljoin
import urllib
import lxml.html as lhtml

class Microdata(object):
	def __init__(self, doc, uri=""):
		self.base = uri
		self.doc = doc
		self.find_base()
		self.cache = {}
		
		# data factory
		self.url = urljoin
		self.datetime = lambda dt: dt
		self.text = lambda t: t
		pass
	
	def items(self, types=None):
		ret = []
		for elem in self.item_elems(self.doc, types):
			item = self.parse_item_elem(elem, {})
			ret.append(item)
			pass
		return ret
	
	def item_elems(self, elem, types=None):
		"iterate top-level items of elements"
		if (elem.get("itemscope") is not None and
			elem.get("itemprop") is None):
			if not types or elem.get("itemtype") in types: yield elem
			pass
		for child in elem.getchildren():
			for _ in self.item_elems(child, types): yield _
			pass
		return
	
	def parse_item_elem(self, elem, item):
		props = {}
		
		refs = elem.get("itemref")
		if refs is not None:
			for ref in refs.split():
				self.parse_item_ref(props, ref)
				pass
			pass
		
		for child in elem.getchildren():
			self.parse_item_props(child, props, None)
			pass
		
		item["properties"] = props
		attrs = elem.keys()
		if "itemid" in attrs: item["id"] = elem.get("itemid")
		if "itemtype" in attrs: item["type"] = elem.get("itemtype")
		return item
	
	def parse_item_ref(self, props, ref):
		if ref not in self.cache:
			self.cache[ref] = {}
			child = self.elem_by_id(self.doc, ref)
			self.parse_item_props(child, {}, ref)
			pass
		
		for name in self.cache[ref]:
			if name not in props: props[name] = []
			props[name].extend(self.cache[ref][name])
			pass
		return
	
	def parse_item_props(self, elem, props, ref):
		if elem is None: return
		propnames = elem.get("itemprop")
		if propnames:
			names = propnames.split()
			value = self.parse_value(elem, ref, names)
			for propname in names:
				if propname not in props: props[propname] = []
				props[propname].append(value)
				pass
			pass
		
		for child in elem.getchildren():
			self.parse_item_props(child, props, ref)
			pass
		return
	
	def parse_value(self, elem, ref, names):
		if elem.get("itemscope") is not None:
			item = {}
			self.store_cache(ref, names, item)
			return self.parse_item_elem(elem, item)
		
		# from http://dev.w3.org/html5/md/#values
		tag = elem.tag
		if tag == "meta": value = self.text(elem.get("content"))
		elif tag in self.src_tags:
			value = self.url(self.base, elem.get("src"))
			pass
		elif tag in self.href_tags:
			value = self.url(self.base, elem.get("href"))
			pass
		elif tag == "object":
			value = self.url(self.base, elem.get("data"))
			pass
		elif tag == "time" and "datetime" in elem.keys():
			value = self.datetime(elem.get("datetime"))
			pass
		else: value = self.text(self.to_text(elem))
		self.store_cache(ref, names, value)
		return value
	
	src_tags = ["audio", "embed", "iframe", "img", "source", "video"]
	href_tags = ["a", "area", "link"]
	
	def store_cache(self, ref, names, value):
		if ref and names:
			for name in names:
				if name not in self.cache[ref]: self.cache[ref][name] = []
				self.cache[ref][name].append(value)
				pass
			pass
		return value
	
	def to_text(self, elem):
		ret = elem.text or ""
		for child in elem.getchildren():
			ret += to_text(child)
			ret += child.tail or ""
			pass
		return ret
	
	def elem_by_id(self, elem, id):
		if elem.get("id") == id: return elem
		for child in elem.getchildren():
			ret = self.elem_by_id(child, id)
			if ret is not None: return ret
			pass
		return None
	
	def find_base(self):
		if self.doc.tag != "html": return
		for head in self.doc.getchildren():
			if head.tag != "head": continue
			for base in head.getchildren():
				if base.tag != "base": continue
				uri = base.get("href")
				if uri is not None:
					self.base = urljoin(self.base, uri)
					return
				pass
			pass
		pass
	pass

class MicrodataParser(object):
	def __init__(self, doc_uri):
		self.doc_uri = doc_uri
		self.html = ""

	def load(self):
		response = urllib.urlopen(self.doc_uri)
		self.html = response.read()
		
	def setHTML(self, html):
		self.html = html

	def dump_items(self):
		"""list microdata as standard data types
		returns [{"properties": {name: [val1, ...], ...}, "id": id, "type": type},
				 ...]
		"""
		if(self.html):
			doc = lhtml.fromstring(self.html)
			return Microdata(doc).items()
		else:
			return None


if __name__ == "__main__":
	from pprint import pprint
	md_doc_URI = "http://schema.org/docs/full_md.html"
	mdp = MicrodataParser(md_doc_URI)
	# mdp.load()
	mdp.setHTML("""
	<div itemscope itemtype="http://schema.org/Event">
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
	""")
	ls = mdp.dump_items()
	pprint(ls)