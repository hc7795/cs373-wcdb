
$(document).ready(
	function() {
		Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');
    	Galleria.run('.galleria_container');
    	Galleria.configure({
    		showInfo : false,
    	});
    }
);