/* Main javascript script to be included on every page. */
$(document).ready(
	function() {


		/* Hovering over an item that should light up. */
		$(".hover_lightup").hover( 
			/* When entering item. */
			function() {
				/* Cache the item's original opacity. If already previously cached however, then ignore. */
				if ( $(this).data("originalOpacity") == undefined ) {
					$(this).data("originalOpacity", $(this).css("opacity") );
				}
				$(this).fadeTo("fast", 1.00);
			}, 
			/* When exiting item. */
			function() {
				$(this).fadeTo("fast", $(this).data("originalOpacity"));
			}
		);


		/* Hovering over an item that should be get underlined. */
		$(".hover_underline").hover( 
			/* When entering item. */
			function() {
				/* Cache the item's original decoration state. If already previously cached however, then ignore. */
				if ( $(this).data("originalDecoration") == undefined ) {
					$(this).data("originalDecoration", $(this).css("text-decoration") );
				}
				$(this).css("text-decoration", "underline");
			}, 
			/* When exiting item. */
			function() {
				$(this).css("text-decoration", $(this).data("originalDecoration"));
			}
		);


		$('.column').masonry({
			columnWidth: 200,
			itemSelector: '.item'
		});
		

	}
);