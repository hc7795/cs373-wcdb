
$(document).ready(
	function() {
		Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');
    	Galleria.run('.index_galleria_container');
    	Galleria.configure({
    		showInfo : false,
    	});
    }
);