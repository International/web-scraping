jQuery(document).ready(function($){
  var swiperA = new Swiper('.swiper-container-ideen', {
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev',
  });
  var swiperB = new Swiper('.swiper-container-home', {
    pagination: '.swiper-pagination',
    paginationClickable: true,
    paginationBulletRender: function (index, className) {
      return '<span class="' + className + '">' + (index + 1) + '</span>';
    },
    autoplay: 4000,
    autoplayDisableOnInteraction: true,
    effect: 'fade',
  });
  $('.flyout').mouseover(function() {
    $('.flyout-container').addClass('open');
  });
  $('.flyout-container').mouseover(function() {
    $(this).addClass('open');
  });
  $('.flyout-container').mouseout(function() {
    $(this).removeClass('open');
  });
  $('.flyout').mouseout(function() {
    $('.flyout-container').removeClass('open');
  });
  //$('.flyout').mouseout(function() {
  //  $('.flyout-container').removeClass('open');
  //});

  $(".menu-toggle").click(function() {
    $('html, body').animate({ scrollTop: 0 }, 0);
    $(".menu-wrapper").addClass("open");
    $(this).hide();
    $(".menu-close").show();
  });
  $(".menu-close").click(function() {
    $(".menu-wrapper").removeClass("open");
    $(this).hide();
    $(".menu-toggle").show();
  });
})