// Кнопка поиска

$(document).ready(function() {
  console.log('123');

  $('[data-fancybox="gallery"]').fancybox({
    // Options will go here
  });

  $('.smoothScroll').on('click',function (e) {
    e.preventDefault();
    var target = this.hash,
    $target = $(target);

   $('html, body').stop().animate({
     'scrollTop': $target.offset().top
    }, 900, 'swing', function () {
     window.location.hash = target;
    });
  });

  $(document).ready(function () {
    $('.animated-icon1,.animated-icon3,.animated-icon4').click(function () {
      $(this).toggleClass('open');
    });
  });
  // Обрез текста
  $('.box__news').each(function () {
    let size = 250;
    let newsText = $(this).text();
    if (newsText.length > size) {
      slicedText = newsText.slice(0, size);
      $(this).text(`${slicedText}...`);
    }
  })

  //owl-carousel initiazilation
  $('.owl-carousel').owlCarousel({
    stagePadding: 50,
    loop: true,
    margin: 10,
    nav: true,
    responsive: {
      320: {
        items: 1
      },
      600: {
        items: 3
      },
      1000: {
        items: 5
      }
    }
  })

  // Просмотр+скачать
  $().fancybox({
    selector: '.owl-item:not(.cloned) a',
    hash: false,
    thumbs: {
      autoStart: true
    },
    buttons: [
      'zoom',
      'download',
      'close'
    ]
  });

  // // Плавная прокрутка

  // new SmoothScroll();

  // function SmoothScroll(el) {
  //   var t = this, h = document.documentElement;
  //   el = el || window;
  //   t.rAF = false;
  //   t.target = 0;
  //   t.scroll = 0;
  //   t.animate = function () {
  //     t.scroll += (t.target - t.scroll) * 0.1;
  //     if (Math.abs(t.scroll.toFixed(5) - t.target) <= 0.47131) {
  //       cancelAnimationFrame(t.rAF);
  //       t.rAF = false;
  //     }
  //     if (el == window) scrollTo(0, t.scroll);
  //     else el.scrollTop = t.scroll;
  //     if (t.rAF) t.rAF = requestAnimationFrame(t.animate);
  //   };
  //   el.onmousewheel = function (e) {
  //     e.preventDefault();
  //     e.stopPropagation();
  //     var scrollEnd = (el == window) ? h.scrollHeight - h.clientHeight : el.scrollHeight - el.clientHeight;
  //     t.target += (e.wheelDelta > 0) ? -70 : 70;
  //     if (t.target < 0) t.target = 0;
  //     if (t.target > scrollEnd) t.target = scrollEnd;
  //     if (!t.rAF) t.rAF = requestAnimationFrame(t.animate);
  //   };
  //   el.onscroll = function () {
  //     if (t.rAF) return;
  //     t.target = (el == window) ? pageYOffset || h.scrollTop : el.scrollTop;
  //     t.scroll = t.target;
  //   };
  // }

  // Счетчик
  $('.counter').counterUp({
    delay: 10,
    time: 1200,
    offset: 70,
    beginAt: 100,
    formatter: function (n) {
      return n.replace(/,/g, '.');
    }
  });
  $('.counter').addClass('animated fadeInDownBig');
  $('h2').addClass('animated fadeIn');


  // Выбрать несколько элементов

  $('.sort').click(function () {
    var mylist = $('.items');
    var listitems = mylist.children('li').get();
    listitems.sort(function (a, b) {
      var compA = $(a).data('selected');
      var compB = $(b).data('selected');
      return (compA < compB) ? 1 : (compA > compB) ? 1 : 0;
    });
    $.each(listitems, function (idx, itm) { mylist.append(itm); });
  })

  $('li', '.items').click(function () {
    var checks = $('[type="checkbox"]', '.checks');
    var item = $(this);

    if (item.data('selected') == '0') {
      item.data('selected', '1');
      item.addClass('selected');
    } else {
      item.data('selected', '0');
      item.removeClass('selected');
    }

    checks.filter('[data-guid="' + item.data('guid') + '"]').prop('checked', item.data('selected') == '1');
  });

  $(document).on('change', '.file-input-field', function () {
    var $value = $(this).parent().next();
    $value.addClass("added").text($(this).val().replace(/C:\\fakepath\\/i, ''));
  });
  $("#phone").mask("+8 (9999) 999 - 99 - 99", { completed: function () { alert("Да, этой мой номер"); } });
  $("#phone2").mask("+8 (9999) 999 - 99 - 99", { completed: function () { alert("Да, этой мой номер"); } });

  // //jQuery plugin
  // (function ($) {

  //   $.fn.uploader = function (options) {
  //     var settings = $.extend({
  //       MessageAreaText: "Вы не выбрали файл.",
  //       // MessageAreaTextWithFiles: "Загруженные файлы:",
  //       DefaultErrorMessage: "Невозможно открыть этот файл.",
  //       BadTypeErrorMessage: "Не верный формат файла!",
  //       acceptedFileTypes: ['pdf', 'jpg', 'doc', 'docx']
  //     }, options);

  //     var uploadId = 1;
  //     //update the messaging
  //     $('.file-uploader__message-area p').text(options.MessageAreaText || settings.MessageAreaText);

  //     //create and add the file list and the hidden input list
  //     var fileList = $('<ul class="file-list"></ul>');
  //     var hiddenInputs = $('<div class="hidden-inputs hidden"></div>');
  //     $('.file-uploader__message-area').after(fileList);
  //     $('.file-list').after(hiddenInputs);

  //     //when choosing a file, add the name to the list and copy the file input into the hidden inputs
  //     $('.file-chooser__input').on('change', function () {
  //       var file = $('.file-chooser__input').val();
  //       var fileName = (file.match(/([^\\\/]+)$/)[0]);

  //       //clear any error condition
  //       $('.file-chooser').removeClass('error');
  //       $('.error-message').remove();

  //       //validate the file
  //       var check = checkFile(fileName);
  //       if (check === "valid") {

  //         // move the 'real' one to hidden list
  //         $('.hidden-inputs').append($('.file-chooser__input'));

  //         //insert a clone after the hiddens (copy the event handlers too)
  //         $('.file-chooser').append($('.file-chooser__input').clone({ withDataAndEvents: true }));

  //         //add the name and a remove button to the file-list
  //         $('.file-list').append('<li style="display: none;"><span class="file-list__name">' + fileName + '</span><button class="removal-button" data-uploadid="' + uploadId + '"></title></button></li>');
  //         $('.file-list').find("li:last").show(800);

  //         //removal button handler
  //         $('.removal-button').on('click', function (e) {
  //           e.preventDefault();

  //           //remove the corresponding hidden input
  //           $('.hidden-inputs input[data-uploadid="' + $(this).data('uploadid') + '"]').remove();

  //           //remove the name from file-list that corresponds to the button clicked
  //           $(this).parent().hide("puff").delay(10).queue(function () { $(this).remove(); });

  //           //if the list is now empty, change the text back
  //           if ($('.file-list li').length === 0) {
  //             $('.file-uploader__message-area').text(options.MessageAreaText || settings.MessageAreaText);
  //           }
  //         });

  //         //so the event handler works on the new "real" one
  //         $('.hidden-inputs .file-chooser__input').removeClass('file-chooser__input').attr('data-uploadId', uploadId);

  //         //update the message area
  //         $('.file-uploader__message-area').text(options.MessageAreaTextWithFiles || settings.MessageAreaTextWithFiles);

  //         uploadId++;

  //       } else {
  //         //indicate that the file is not ok
  //         $('.file-chooser').addClass("error");
  //         var errorText = options.DefaultErrorMessage || settings.DefaultErrorMessage;

  //         if (check === "badFileName") {
  //           errorText = options.BadTypeErrorMessage || settings.BadTypeErrorMessage;
  //         }

  //         $('.file-chooser__input').after('<p class="error-message">' + errorText + '</p>');
  //       }
  //     });

  //     var checkFile = function (fileName) {
  //       var accepted = "invalid",
  //         acceptedFileTypes = this.acceptedFileTypes || settings.acceptedFileTypes,
  //         regex;

  //       for (var i = 0; i < acceptedFileTypes.length; i++) {
  //         regex = new RegExp("\\." + acceptedFileTypes[i] + "$", "i");

  //         if (regex.test(fileName)) {
  //           accepted = "valid";
  //           break;
  //         } else {
  //           accepted = "badFileName";
  //         }
  //       }

  //       return accepted;
  //     };
  //   };
  // }(jQuery));

  // //init
  // $(document).ready(function () {
  //   $('.fileUploader').uploader({
  //     MessageAreaText: "Прикрепить файлы"
  //   });
  // });

  $('#toggle_panel').click(function(event){
    event.preventDefault();
    $('.admin_panel').toggle();
    if ($('.admin_panel').is(":visible")) {
      $('#toggle_panel').html('<i class="fas fa-arrow-up"></i>');
    } else {
      $('#toggle_panel').html('<i class="fas fa-arrow-down"></i>');
    }
  });
});