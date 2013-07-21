/* Main javascript script to be included on every page. */
$(document).ready(
	function() {

		$('.column').masonry({
			columnWidth: 200,
			itemSelector: '.item'
		});
	}
);