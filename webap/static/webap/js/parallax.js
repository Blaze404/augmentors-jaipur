
    $(window).scroll(function(){
       	var scroll_position = $(window).scroll();
       	$('.section').css({
       		'background-position-x' : + scroll_position + 'px';
       	})

    })