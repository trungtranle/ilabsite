(function($) {
	"use strict"

	// Scrollspy
	$('body').scrollspy({
		target: '#nav-menu-container',
		offset: $(window).height() / 2
	});

	$(document).ready(function(){
	    $('iframe#map_frame').attr('src', "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.6189897830086!2d106.66220724978443!3d10.763819092292406!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752eef537bf73f%3A0x70294fc6e9bcdd30!2zMTcxIE5o4bqtdCBU4bqjbywgUGjGsOG7nW5nIDYsIFF14bqtbiAxMCwgSOG7kyBDaMOtIE1pbmgsIFZpZXRuYW0!5e0!3m2!1sen!2s!4v1542775058466");    
	});

})(jQuery);
