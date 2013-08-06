
$(document).ready(
	function() {
		Galleria.loadTheme('../static/galleria_themes/classic/galleria.classic.min.js');

    	Galleria.configure({
    		showInfo : false,
    		autoplay : true,
    		transition : 'fade',
    		debug : false
    	});

    	/* Display corresponding content when galleria finishes loading a new image. */
    	Galleria.ready(function() {
    		this.bind("loadstart", function(e) {
    			var dataObject = this.getData(this.getIndex());
                var currentImage = dataObject.original;
                var $imageName = $(currentImage).attr('name');
                var $imageType = $(currentImage).attr('type');
                var parentElement = '.' + $imageType + '_information';

		        $(parentElement + " h3").animate({
				    opacity: 0.0,
				    duration: "slow"
				});
				$(parentElement + " p").animate({
				    opacity: 0.0,
				    duration: "slow"
				});
		    });

		    this.bind("image", function(e) {
		    	var dataObject = this.getData(this.getIndex());
                var currentImage = dataObject.original;
                var $imageName = $(currentImage).attr('name');
                var $imageType = $(currentImage).attr('type');
                var $imageText = $(currentImage).attr('text');
                var $imageSlug = $(currentImage).attr('slug');
                var parentElement = '.' + $imageType + '_information';

                $(parentElement).attr("href", "/" + $imageType + "/" + $imageSlug);
		        $(parentElement + " h3").html($imageName);
		        $(parentElement + " p").html($imageText);

		        $(parentElement + " h3").animate({
				    opacity: 1.0,
				    duration: "fast"
				});
				$(parentElement + " p").animate({
				    opacity: 1.0,
				    duration: "fast"
				});

		    });
		});

    	Galleria.run('.index_galleria_container');
    }
);