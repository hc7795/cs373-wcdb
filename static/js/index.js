/* Main javascript script to be included on every page. */

$(document).ready( function() { 
	var container = document.querySelector('#myContent');
	var msnry = new Masonry( container, {
	  columnWidth: 15,
	  itemSelector: 'item'
	});
});

