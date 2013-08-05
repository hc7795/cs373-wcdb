/* Main javascript script to be included on every page. */
$(document).ready(
	function() {
		Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');
    	Galleria.run('.common_galleria');
    	Galleria.configure({
    		showInfo : false,
    		dataSort : 'random',
    	});
    }
);
