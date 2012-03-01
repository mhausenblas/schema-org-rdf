var SCHEMA_ORG_BASE = 'http://schema.org/';
var rdf; // see http://code.google.com/p/rdfquery/wiki/RdfPlugin for documentation
var num_triples = 0;
var current_concept;
var parent_concept = 'Thing';

////////////////////////////////////////////////////
// Schema.org extensions metadata
//
var EXTENSIONS_SCHEMA = {
	'base' : 'http://schema.org/extensions/meta#',
	'prefix' : 'schema-e',
	'state' : {
		'published' : 'Has been integrated into Schema.org and is hence available under http://schema.org/extensions now.', 
		'candidate' : 'Requires a Last Call, had some good review, and is now considered to be published soon-ish.', 
		'proposal' : 'Requires at least some sort of proposal of the terms, on the Wiki or via the mailing list, etc.', 
		'discussion' : 'No proposal yet, but some expression of interest and typically a discussion (on IRC, Wiki, mailing list, etc.) around it.'
	}
};

// The description of the extensions - should be pulled in live from a Web service that extract the 
// information from http://www.w3.org/wiki/WebSchemas/SchemaDotOrgProposals and/or another data source TBD.
var extensions = [
{
	'id' : 'http://schema.org/extensions/jobpostings', // the globally unique extension identifier
	'state' : 'schema-e:published', // state of the extension, see extensions_schema, above
	'title' : 'Job Postings', // short title, what is called 'Topic' in http://www.w3.org/wiki/WebSchemas/SchemaDotOrgProposals
	'description' : 'A type for job adverts.', //summary of the extension's purpose and/or terms, what is called Summary in http://www.w3.org/wiki/WebSchemas/SchemaDotOrgProposals
	'spec' : 'http://www.w3.org/wiki/JobPostingSchema'	// for all above schema-e:discussion, this provides a pointer to the 
														// full specification of the terms on the Wiki or externally which must resolve (!)
														// however, for extensions in their early days this might well be only an URL to a tweet or the like.
},
{
	'id' : 'http://schema.org/extensions/iptc-rnews',
	'state' : 'schema-e:published',
	'title' : 'IPTC/rNews integration',
	'description' : 'Integration of the rNews vocabulary produced by the IPTC.',
	'spec' : 'http://dev.iptc.org/rNews-10-Implementation-Guide-HTML-5-Microdata'
},
{
	'id' : 'http://schema.org/extensions/tv-radio',
	'state' : 'schema-e:candidate',
	'title' : 'TV and Radio',
	'description' : 'Proposes modest changes and additions to support TV and radio (from EBU and BBC).',
	'spec' : 'http://www.w3.org/wiki/TVRadioSchema'
},
{
	'id' : 'http://schema.org/extensions/comics',
	'state' : 'schema-e:candidate',
	'title' : 'Comics and Serials',
	'description' : 'Proposal from Marvel.',
	'spec' : 'http://www.w3.org/wiki/PeriodicalsComics'
},
{
	'id' : 'http://schema.org/extensions/web-apps',
	'state' : 'schema-e:proposal',
	'title' : 'Software Application',
	'description' : 'A class for Software Applications - webapps, both installable and Web-based.',
	'spec' : 'http://www.w3.org/wiki/SoftwareApplicationSchema'
},
{
	'id' : 'http://schema.org/extensions/real-estate',
	'state' : 'schema-e:discussion',
	'title' : 'Real Estate',
	'description' : 'Enthusiastic discussion in favour of adding RealEstate support. Tracked as ISSUE-13.',
	'spec' : 'http://www.w3.org/wiki/RealEstate'
}
];

//TODO: test http://viejs.org/

$(function() {
	show_nav();
	$('#ext-states').tabs(); // create the extension tabs
	
	// explore mode:
	$('#explore').click(function() {
		$('#nav-output').show('slow', function() {
			if(num_triples == 0){ // init, count triples
				rdf = $('div').rdf(); // extract all RDFa markup from any div
				all_triples(rdf, false); // generic processing of all triples; currently just counts it
			}
			render_toplevel_things(rdf);
			hide_nav();
		});
	});

	$('#close-explore').live("click", function() {
		$('#subconcepts').hide();
		$('#nav-output').slideUp('slow');
		show_nav();
	});
	
	$(".lnk a").live("click", function(){
		var conceptID = $(this).attr('href').toString().substring('#__'.length);
		render_concept(rdf, conceptID);
	});
	
	$(".lnk .expand").live("click", function(){
		var conceptID = $(this).attr('id').toString().substring('expand___'.length);
		render_concept(rdf, conceptID);
		// $('#__'+conceptID).focus();
	});
	

	// extensions mode:
	$('#extensions').click(function() {
		render_extensions();
		$('#ext-output').slideDown('slow');
		hide_nav();
	});
	
	$('#close-ext').click(function() {
		$('#ext-output').slideUp('slow');
		show_nav();
	});
	
	
});

function render_concept(rdf, conceptID){
	var things = []; // the things (direct sub-classes of concept)
	
	rdf
	.prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
	.where('?s rdfs:subClassOf <http://schema.org/'+ conceptID + '>')
	.each(function () {
		if($.inArray(this.s.value, things) == -1){ // not already in the seen list, remember each subject only once
			things.push(this.s.value);
		}
	});
	
	$('#subconcepts').html('<h3>' + conceptID + '</h3><p class="concept-stats">This concept has ' + things.length +' sub-concepts and Y extensions.</p>');
	//parent_concept = conceptID;
	// TODO: add two tabs: one for core and one for extensions
	
	// present things in alphabetical order
	things.sort(); 
	for(i=0; i < things.length; i++){
		var t = things[i].toString().substring(SCHEMA_ORG_BASE.length);
		var t_id = '__'+ t;
		if($('#'+t_id).length == 0) { // add an anchor if not yet exists
			$('<div class="dynanchor" id="' + t_id + '" >&middot;</div>').insertBefore('div[about|="'+ things[i]  + '"]'); // find the div and add an @id before
		}
		$('#subconcepts').append('<div class="lnk"><span class="expand" id="expand_' +  t_id + '" title="expand this concept">&laquo;</span><span><a href="#' + t_id +'">' + t + '</a></span></div>'); // build result
	}
}

function render_toplevel_things(rdf){
	var toplevel_things = []; // the top level things (direct sub-classes of schema:Thing)
	var result = '<span id="close-explore">x</span>'
	result = result + '<div id="subconcepts"></div>';
	result = result + '<div id="top-level-concepts"><h3>Top-level concepts</h3><p class="concept-stats">A top-level concept is one that is directly derived from schema:Thing</p>';

	rdf
	.prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
	.where('?s rdfs:subClassOf <http://schema.org/Thing>')
	.each(function () {
		if($.inArray(this.s.value, toplevel_things) == -1){ // not already in the seen list, remember each subject only once
			toplevel_things.push(this.s.value);
		}
	});
	
	// present the top-level things in alphabetical order:
	toplevel_things.sort(); 
	for(i=0; i < toplevel_things.length; i++){
		var t = toplevel_things[i].toString().substring(SCHEMA_ORG_BASE.length);
		var t_id = '__'+ t;
		$('<div class="dynanchor" id="' + t_id + '" >&middot;</div>').insertBefore('div[about|="'+ toplevel_things[i]  + '"]'); // find the div and add an @id before
		result = result + '<div class="lnk"><span class="expand" id="expand_' +  t_id + '" title="expand this concept">&laquo;</span><span><a href="#' + t_id +'">' + t + '</a></span></div>'; // build result
	}	
	$('#nav-output').html(result);
}

function render_extensions(){
	// handling of extensions:
	$('#tabs-published').html('<p class="ext-state">' +  EXTENSIONS_SCHEMA.state.published + '</p>');
	for(i=0; i < extensions.length; i++){ // published extensions
		if(extensions[i].state == (EXTENSIONS_SCHEMA.prefix + ':published')) {
			$('#tabs-published').append('<div class="extension"><a class="expand" href="' + extensions[i].id + '">&laquo;</a> ' + extensions[i].title + ': <a href="' + extensions[i].spec +'">schema</a></div>');
		}
	}
	$('#tabs-candidate').html('<p class="ext-state">' +  EXTENSIONS_SCHEMA.state.candidate + '</p>');
	for(i=0; i < extensions.length; i++){ // candidate extensions
		if(extensions[i].state == (EXTENSIONS_SCHEMA.prefix + ':candidate')) {
			$('#tabs-candidate').append('<div class="extension"><a class="expand" href="' + extensions[i].id + '">&laquo;</a> ' + extensions[i].title + '</span>: <a href="' + extensions[i].spec +'">schema</a></div>');
		}
	}
	$('#tabs-proposal').html('<p class="ext-state">' +  EXTENSIONS_SCHEMA.state.proposal + '</p>');
	for(i=0; i < extensions.length; i++){ // // proposal extensions
		if(extensions[i].state == (EXTENSIONS_SCHEMA.prefix + ':proposal')) {
			$('#tabs-proposal').append('<div class="extension"><a class="expand" href="' + extensions[i].id + '">&laquo;</a> ' + extensions[i].title + '</span>: <a href="' + extensions[i].spec +'">proposal</a></div>');
		}
	}
	$('#tabs-discussion').html('<p class="ext-state">' +  EXTENSIONS_SCHEMA.state.discussion + '</p>');
	for(i=0; i < extensions.length; i++){ // extensions under discussion
		if(extensions[i].state == (EXTENSIONS_SCHEMA.prefix + ':discussion')) {
			$('#tabs-discussion').append('<div class="extension"><a class="expand" href="' + extensions[i].id + '">&laquo;</a> 	' + extensions[i].title + '</span>: <a href="' + extensions[i].spec +'">discussion</a></div>');
		}
	}
}

function hide_nav(){
	$('#nav').slideUp('fast');
}

function show_nav(){
	$('#nav').slideDown('slow');
}

function all_triples(rdf, do_log){
	rdf
	.where('?s ?p ?o')
	.each(function () {
		if(do_log) console.log(this.s + ' ' + this.p + ' ' + this.o);
		num_triples = num_triples + 1;
	});
	console.log('Parsed ' + num_triples + ' triples');
}