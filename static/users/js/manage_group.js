(function ($) {
    "use strict";

    /* Mixitup */
    $(function() {
        var containerEl = document.querySelector('.member_list');
        var mixer = mixitup(containerEl);
    });
    
    $(document).on('click', '.member__item__trigger', function () {
        $('.member__item__trigger').removeClass('active');
        $(this).addClass('active');
    });

})(jQuery);