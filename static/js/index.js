/* Main javascript script to be included on every page. */

$(document).ready( function() { 
	var container = document.querySelector('#container');
	var msnry = new Masonry( container, {
	  itemSelector: 'item',
	  columnWidth: container.querySelector('.grid-sizer')
	});
});

