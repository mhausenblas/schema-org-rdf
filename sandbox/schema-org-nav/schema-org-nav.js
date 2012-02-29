var SCHEMA_ORG_BASE = 'http://schema.org/';
var rdf; // see http://code.google.com/p/rdfquery/wiki/RdfPlugin for documentation
var num_triples = 0;

$(function() {
	rdf = $('div').rdf(); // extract all RDFa markup from any div
	all_triples(rdf, false); // generic processing of all triples; currently just counts it
	show_nav();
	
	$('#explore').click(function() {
 		render_toplevel_things(rdf);
		hide_nav();
	});

	$(".lnk a").live("click", function(){
		var targetID = $(this).attr('href');
		$('#'+targetID).css('border', '1px solid #ff3333');
//		return true;
	});
	
	$(".lnk .expand").live("click", function(){
		var conceptID = $(this).attr('id').toString().substring('expand___'.length);
		render_concept(rdf, conceptID, 'Thing');
	});
	
});


function render_concept(rdf, conceptID, parentID){
	var things = []; // the things (direct sub-classes of concept)
	
	$('#subconcepts').html('<h3>' + parentID + ' : ' + conceptID + "</h3>");
	
	rdf
	.prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
	.where('?s rdfs:subClassOf <http://schema.org/'+ conceptID + '>')
	.each(function () {
		if($.inArray(this.s.value, things) == -1){ // not already in the seen list, remember each subject only once
			things.push(this.s.value);
		}
	});
	// present things in alphabetical order
	things.sort(); 
	for(i=0; i < things.length; i++){
		var t = things[i].toString().substring(SCHEMA_ORG_BASE.length);
		var t_id = '__'+ t;
		$('<div class="dynanchor" id="' + t_id + '" >&middot;</div>').insertBefore('div[about|="'+ things[i]  + '"]'); // find the div and add an @id before
		$('#subconcepts').append('<div class="lnk"><span class="expand" id="expand_' +  t_id + '" title="expand this concept">&laquo;</span><span><a href="#' + t_id +'">' + t + '</a></span></div>'); // build result
	}
}

function render_toplevel_things(rdf){
	var toplevel_things = []; // the top level things (direct sub-classes of schema:Thing)
	$('#nav-output').html('<h3>Top-level concepts</h3>');
	$('#nav-output').slideDown('slow');
	rdf
	.prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
	.where('?s rdfs:subClassOf <http://schema.org/Thing>')
	.each(function () {
		if($.inArray(this.s.value, toplevel_things) == -1){ // not already in the seen list, remember each subject only once
			toplevel_things.push(this.s.value);
		}
	});
	// present the top-level things in alphabetical order
	toplevel_things.sort(); 
	for(i=0; i < toplevel_things.length; i++){
		var t = toplevel_things[i].toString().substring(SCHEMA_ORG_BASE.length);
		var t_id = '__'+ t;
		$('<div class="dynanchor" id="' + t_id + '" >&middot;</div>').insertBefore('div[about|="'+ toplevel_things[i]  + '"]'); // find the div and add an @id before
		$('#nav-output').append('<div class="lnk"><span class="expand" id="expand_' +  t_id + '" title="expand this concept">&laquo;</span><span><a href="#' + t_id +'">' + t + '</a></span></div>'); // build result
	}
	$('#nav-output').append('<div id="subconcepts" />');
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