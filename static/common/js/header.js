(function ($) {
    "use strict";
    /*Dropdown Menu*/
    $('.dropdown').click(function () {
        $(this).attr('tabindex', 1).focus();
        $(this).toggleClass('active');
        $(this).find('.dropdown-menu').slideToggle(300);
    });
    $('.dropdown').focusout(function () {
        $(this).removeClass('active');
        $(this).find('.dropdown-menu').slideUp(300);
    });
    $('.dropdown .dropdown-menu li').click(function () {
        $(this).parents('.dropdown').find('span').text($(this).text());
        $(this).parents('.dropdown').find('input').attr('value', $(this).attr('id'));
    });
    /*End Dropdown Menu*/


    $('.dropdown-menu li').click(function () {
    var input = '<strong>' + $(this).parents('.dropdown').find('input').val() + '</strong>',
    msg = '<span class="msg">Hidden input value: ';
    $('.msg').html(msg + input + '</span>');
    }); 

    /* User Info */
    var user_info = $('.user__info')[0];
    $('.user__info__toggle').click(function () {
        $(user_info).toggleClass('hidden__user__info');
    });


    /* Mixitup */
    // $(function() {
    //     var containerEl = document.querySelector('.car__item_list');
    //     var mixer = mixitup(containerEl);
    // });
    
    // $(document).on('click', '.car__item__trigger', function () {
    //     $('.car__item__trigger').removeClass('active');
    //     $(this).addClass('active');
    // });

    /* submit */
    var date_input =  $('.validate__date__input');
    $('.validate__form').on('submit',function(){
        var check = false;
        if($(date_input[0]).val() < $(date_input[1]).val()){
            return true;
        }
        else{
            alert("時間指定に誤りがあります");
            return false;
        }
    });

})(jQuery);
