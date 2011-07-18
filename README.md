# Schema.RDFS.org

This is a project to provide an RDF(S) version of Schema.org terms, including tools, examples and mappings to benefit from data that uses Schema.org terms. Currently, we have the following sub-projects (in descending order of maturity):

* Generating variants
* Schema.org gateway
* Examples
* Mappings

## Sub-projects

Over time, a number of sub-projects of Schema.RDFS.org emerged, introduced in the following. Have a look at the respective directories for more details.

### Generating variants
[This](https://github.com/mhausenblas/schema-org-rdf/tree/master/scrapers) Schema.RDFS.org sub-project deals with generating structured representations for Schema.org terms through the natural language definition found in Schema.org.

### Schema.org gateway

[This](https://github.com/mhausenblas/schema-org-rdf/tree/master/tools/schema-gateway) Schema.RDFS.org sub-projec develops the Schema.org gateway, a anything-to-anything data format converter, based on the [Lingua Franca](http://c2.com/cgi/wiki?LinguaFrancaPattern "Lingua Franca Pattern") pattern.

### Examples

[This](https://github.com/mhausenblas/schema-org-rdf/tree/master/examples) Schema.RDFS.org sub-project collects Schema.org examples in all kinds of markup and data formats, incl. RDFa, CSV, JSON etc.

### Mappings

[This](https://github.com/mhausenblas/schema-org-rdf/tree/master/mappings) Schema.RDFS.org sub-project collects mappings to Schema.org terms from widely deployed Linked Data vocabularies such as Dublin Core, FOAF, GoodRelations, SIOC, DBpedia ontology, etc.

## Who is behind this?

Led by [Michael](http://sw-app.org/mic.xhtml#i) and [Richard](http://richard.cyganiak.de/foaf.rdf#cygri) of the Linked Data Research Centre, [DERI](http://www.deri.ie) the Schema.RDFS.org project is officially endorsed and supported by the EC FP7 LOD-Around-The-Clock Support Action (<a href="http://latc-project.eu/">LATC</a>). Many people from the Linked Data domain, Web of Data domain and other communities (SEO, library, archives, etc.) are contributing and have been delivering valuable input.

If you have any questions, please do not hesitate to ask Michael, either via [michael.hausenblas AT gmail.com](mailto:&#x6D;&#x69;&#x63;&#x68;&#x61;&#x65;&#x6C;&#x2E;&#x68;&#x61;&#x75;&#x73;&#x65;&#x6E;&#x62;&#x6C;&#x61;&#x73;&#x40;&#x67;&#x6D;&#x61;&#x69;&#x6C;&#x2E;&#x63;&#x6F;&#x6D;) or via Twitter where he listens to [@mhausenblas](http://twitter.com/mhausenblas/) or drop by at the [#swig](http://chatlogs.planetrdf.com/swig/) channel on Freenode/IRC.

## License

The software and artefacts (such as examples, mappings, etc.) provided through the Schema.RDFS.org project are, if not otherwise stated, in the Public Domain.

## Roadmap and Ideas

* Community
	* get communities involved and give them a sense of ownership (ML, Twitter, here, etc.)
	* feedback on a Wiki, issue tracker, etc. (?)
* Generating variants
	* multi-lang labels/comments
	* mappings to well-known legacy terms
* Schema.org gateway
	* http://bibutils.refbase.org/ extensions and collaboration
* Examples
	* collect
	* create based on existing examples
* Mappings
	* multi-lang suggestions into a Google spreadsheet?
	* Alexandre will provide SIOC mapping, hosted directly here
	* ask vocab stake-holders to provide pointers to their mapping (Michael: DBpedia, FOAF, DC, GR, Richard: the rest ;)