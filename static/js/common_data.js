/* Main javascript script to be included on every page. */
$(document).ready(
	function() {
		Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');
    	Galleria.configure({
    		showInfo : false,
    		dataSort : 'random',
    		autoplay : true,
    		transition : 'fade',
    		debug : false,
    	});
    	Galleria.run('.common_galleria');


        /* Add expand class to every overflowing object. */
        // var items = document.all;
        // for (var i = 0; i < items.length; i++) {
        //     var $this = items[i];

        //     if ($this.offsetWidth < $this.scrollWidth) {
        //         $($this).addClass("expand")
        //     }

        //     ++i;
        // }
        $(".ellipsis").each(function() {

            if ($(this).children().last().text().indexOf('...') > -1) {
                $(this).addClass('clickToExpand');
                $(this).hover(function(){
                    $(this).toggleClass('ellipsis_hover');
                });
            }
        });

        $('.clickToExpand').click(function() {
            $(this).toggleClass('clickToCollapse', "fast", "easeInQuad");            
        });
    }

);

