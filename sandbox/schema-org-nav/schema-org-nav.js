var SCHEMA_ORG_BASE = 'http://schema.org/';
var rdf;
var num_triples = 0;

$(function() {
	// init - see http://code.google.com/p/rdfquery/wiki/RdfPlugin for documentation
	rdf = $('div').rdf(); // extract all RDFa markup from any div
	all_triples(rdf, false); // generic processing of all triples; currently just counts it
	$('#nav').slideDown('slow');

	$('#explore').click(function() {
 		render_toplevel_things(rdf);
		hide_nav();
	});

	$(".lnk a").live("click", function(){
		var targetID = $(this).attr('href');
		$('#'+targetID).css('border', '1px solid #ff3333');
//		return true;
	});
});

function render_toplevel_things(rdf, do_log){
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
		$('#nav-output').append('<div class="lnk"><a href="#' + t_id +'">' + t + '</a></div>'); // build result
	}
}

function hide_nav(){
	$('#nav').slideUp('fast');
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