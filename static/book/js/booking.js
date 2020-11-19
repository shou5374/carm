'use strict';

(function ($) {

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


    /*==================================================================
    [ Schedule ]*/

    $('.schedule__item').click(function () {
        $(this).children('.schedule__times').toggleClass('hidden__block');
    });

})(jQuery);