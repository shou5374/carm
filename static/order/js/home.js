'use strict';

(function ($) {

    /*==================================================================
    [ Mixt up ]*/
    $(function() {
        var containerEl = document.querySelector('.car__item__list');
        var mixer = mixitup(containerEl);
    });
    
    $(document).on('click', '.car__item__toggle', function () {
        $('.car__item__toggle').removeClass('active');
        $(this).addClass('active');
    });

    /*==================================================================
    [ Modal ]*/
    $('.open__modal').click(function(){
        var id = $(this).attr('id');
        var modal_id = "#modal__area__" + id
        $(modal_id).fadeIn();
    });

    $('.close__modal , .modal__background').click(function(){
        var id = $(this).attr('id');
        var modal_id = "#modal__area__" + id.split('--')[1]
        $(modal_id).fadeOut();
    });

})(jQuery);