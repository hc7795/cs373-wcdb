/* Main javascript script to be included on every page. */
$(document).ready(
	function() {
		// Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');
    	Galleria.configure({
    		showInfo : false,
    		dataSort : 'random',
    		autoplay : true,
    		transition : 'fade',
    		debug : false,
            thumbnails: 'lazy'
    	});
    	Galleria.run('.common_galleria');

        $('.ellipsis_container').each(function() {

            if ($(this).text().indexOf('...') > -1) {

                $(this).addClass('clickToExpand');
                $(this).hover(function() {
                    $(this).toggleClass('ellipsis_hover');
                });
            }
        });

        $('.clickToExpand').click(function() {
            $(this).toggleClass('clickToCollapse', "fast", "easeInQuad"); 


            console.log($(this).children());
            console.log($(this).children().children('.add_ellipsis').text());
            console.log($(this).children().children('.no_ellipsis').text());

            $(this).children().children('.add_ellipsis').toggle("slow");    
            $(this).children().children('.no_ellipsis').toggle("fast"); 
        });

        $( ".clickToExpand" ).tooltip({ content:"Click to expand/collapse.", items:"div"});

    }

);

