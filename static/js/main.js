/* Main javascript script to be included on every page. */



/* Returns true if the element overflows its parent. */
$.fn.hasOverflow = function() {
    var $this = $(this);
    var $children = $this.find('*');
    var len = $children.length;

    if (len) {
        var maxWidth = 0;
        var maxHeight = 0
        $children.map(function(){
            maxWidth = Math.max(maxWidth, $(this).outerWidth(true));
            maxHeight = Math.max(maxHeight, $(this).outerHeight(true));
        });

        return maxWidth > $this.width() || maxHeight > $this.height();
    }

    return false;
};





/* Runs when document is fully loaded. */
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

		/* Perform ellipsis if necessary on anything with the ellipsis class. */
		$('.ellipsis_container').ellipsis(".add_ellipsis");

	}
);
