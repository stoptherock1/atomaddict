var changeSignPages = function() {
		/* push the container-box to the right */
		$('.btn-sign-up').click(function() {
			var sign_in = $('.container-box-sign-in');
			var sign_up = $('.container-box-sign-up');
			
 			sign_in.animate({
 				left: "-100%"
 			}, 400);
 			
 			sign_up.animate({
 				left: "0%"
 			}, 400);
		});
		
		$('.btn-sign-in').click(function() {
			var sign_in = $('.container-box-sign-in');
			var sign_up = $('.container-box-sign-up');
			
			sign_up.animate({
				left: "100%"
			}, 400);
			
			sign_in.animate({
				left: "0%"
			}, 400);
			
		});
		
	};
	
	$(document).ready(changeSignPages);