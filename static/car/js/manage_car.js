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

    /*==================================================================
    [ Preview car image ]*/
    $(function() {
      
        // アップロードするファイルを選択
        $('input[type=file]').change(function() {
          var file = $(this).prop('files')[0];

          console.log(file)
      
          // 画像以外は処理を停止
          if (! file.type.match('image.*')) {
            // クリア
            $(this).val('');
            return;
          }
      
          // 画像表示
          var reader = new FileReader();
          reader.onload = function() {
            var img_src = $('<img>').attr('src', reader.result);
            img_src.addClass('preview__img')
            $('.preview__img__space').html(img_src);
          }
          reader.readAsDataURL(file);
        });
      });

})(jQuery);