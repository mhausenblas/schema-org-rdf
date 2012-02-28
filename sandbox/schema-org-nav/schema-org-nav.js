// using https://github.com/linkeddata/rdflib.js seems not to work:
//var kb = new $rdf.Formula();
//var doc;
//var t = $rdf.rdfa.parse('div[typeof|="rdfs:Class"]', kb, "http://schema.org", doc);
// for (i=0; i < kb.statements.length; i++) {
// 	var s = kb.statements[i].subject;
// 	var p = kb.statements[i].predicate;
// 	var o = kb.statements[i].object;
// 	$('#nav-output').append('Triple:' + s + ' ' + p + ' ' + o);
// }

var SCHEMA_ORG_BASE = 'http://schema.org/';


$(function() {	
	$('#explore').click(function() {
		var rdf = $('div').rdf(); // extract all RDFa markup from any div
		var things = []; // remember the things that we already have in the result
		rdf
		.where('?s ?p ?o')
		.each(function () {
			if($.inArray(this.s.value, things) == -1){ // not already in the list of things we've outputted ...
				var t = this.s.value.toString().substring(SCHEMA_ORG_BASE.length);
				var t_id = '__'+ t;
				$("<div id='" + t_id + "' class='hidden-anchor' />").insertBefore('div[about|="'+ this.s.value  + '"]'); // find the div and add an @id before
				$('#nav-output').append('<div class="lnk" id="lnk_' + t_id +'">' + t + '</div>'); // build result
				things.push(this.s.value);
			}
			
		});
		$('#nav-output').slideDown('slow');
	});

	$('.lnk').live('click', function() {
		var target = $(this).attr('id');
		target = target.toString().substring('lnk_'.length);
		console.log('prepare to jump to ' + target);
		$('#'+target).ScrollTo();
	});
});