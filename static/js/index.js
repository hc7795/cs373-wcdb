
$(document).ready(
	function() {
		Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');	
    	Galleria.configure({
    		showInfo : false,
    		autoplay : true,
    		transition : 'fade',
    	});
    	Galleria.run('.index_galleria_container');
    }
);