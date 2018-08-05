// Function for pagetop.
$(function() {
  var topBtn;
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
