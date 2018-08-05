// Prevent sending when return key is pressed on input form.
$('#myform').on('sumbit', function(e) {
  e.preventDefault();
});

// Prevent continuous transmission.
$('.save').on('click', function(e) {
  $('.save').addClass('disabled');
  $('#myform').submit();
});

// Display control for cancel search button.
conditions = $('#filter').serializeArray();
$.each(conditions, function() {
  if (this.value) {
    $('.filtered').css('visibility', 'visible');
  }
});

// Function for pagetop.
$(function() {
  var topBtn;
  topBtn = void 0;
  topBtn = $('#pagetop');
  topBtn.hide();
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      topBtn.fadeIn();
    } else {
      topBtn.fadeOut();
    }
  });
  topBtn.click(function() {
    $('body,html').animate({
      scrollTop: 0
    }, 1000);
    return false;
  });
});
