(function ($) {

  "use strict";

  // init jarallax parallax
  var initJarallax = function () {
    jarallax(document.querySelectorAll(".jarallax"));

    jarallax(document.querySelectorAll(".jarallax-img"), {
      keepImg: true,
    });
  }

  // input spinner
  var initProductQty = function(){

    $('.product-qty').each(function(){

      var $el_product = $(this);
      var quantity = 0;

      $el_product.find('.quantity-right-plus').click(function(e){
          e.preventDefault();
          var quantity = parseInt($el_product.find('.quantity').val());
          $el_product.find('.quantity').val(quantity + 1);
      });

      $el_product.find('.quantity-left-minus').click(function(e){
          e.preventDefault();
          var quantity = parseInt($el_product.find('.quantity').val());
          if(quantity>0){
            $el_product.find('.quantity').val(quantity - 1);
          }
      });

    });

  }

  // init Chocolat light box
  var initChocolat = function() {
    $('.chocolat-parent').Chocolat();
};

$(document).ready(function() {
    initChocolat();
});

$(window).on('load', function(){
    $('.preloader').fadeOut();
});

  // Animate Texts
  var initTextFx = function () {
    $('.txt-fx').each(function () {
      var newstr = '';
      var count = 0;
      var delay = 0;
      var stagger = 10;
      var words = this.textContent.split(/\s/);
      
      $.each( words, function( key, value ) {
        newstr += '<span class="word">';

        for ( var i = 0, l = value.length; i < l; i++ ) {
          newstr += "<span class='letter' style='transition-delay:"+ ( delay + stagger * count ) +"ms;'>"+ value[ i ] +"</span>";
          count++;
        }
        newstr += '</span>';
        newstr += "<span class='letter' style='transition-delay:"+ delay +"ms;'>&nbsp;</span>";
        count++;
      });

      this.innerHTML = newstr;
    });
  }

  $(document).ready(function () {

    initProductQty();
    initJarallax();
    initChocolat();
    initTextFx();

    $(".user-items .search-item").click(function () {
      $(".search-box").toggleClass('active');
      $(".search-box .search-input").focus();
    });
    $(".close-button").click(function () {
      $(".search-box").toggleClass('active');
    });

    var breakpoint = window.matchMedia('(max-width:61.93rem)');

    if (breakpoint.matches === false) {
      
      var swiper = new Swiper(".main-swiper", {
        slidesPerView: 1,
        spaceBetween: 48,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        breakpoints: {
          900: {
            slidesPerView: 2,
            spaceBetween: 48,
          },
        },
      });

      $('.quantity-left-minus').click(function(e) {
        e.preventDefault();
        var quantity = parseInt($(this).siblings('.input-number').val());
        if (quantity > 1) {
            $(this).siblings('.input-number').val(quantity - 1);
            updateCart($(this).data('cart-item-id'), quantity - 1);
        }
    });

    $('.quantity-right-plus').click(function(e) {
        e.preventDefault();
        var quantity = parseInt($(this).siblings('.input-number').val());
        $(this).siblings('.input-number').val(quantity + 1);
        updateCart($(this).data('cart-item-id'), quantity + 1);
    });

    // Event listener for remove item button
    $('.remove-item').click(function(e) {
        e.preventDefault();
        var cartItemId = $(this).data('cart-item-id');
        removeFromCart(cartItemId);
        $(this).closest('.cart-item').remove();
    });

    // Function to update cart
    function updateCart(cartItemId, quantity) {
        $.ajax({
            url: '/update_cart/' + cartItemId + '/' + quantity + '/',
            method: 'GET',
            success: function(response) {
                console.log('Cart updated');
            }
        });
    }

    // Function to remove item from cart
    function removeFromCart(cartItemId) {
        $.ajax({
            url: '/remove_from_cart/' + cartItemId + '/',
            method: 'GET',
            success: function(response) {
                console.log('Item removed from cart');
            }
        });
    }

      // homepage 2 slider
      var swiper = new Swiper(".thumb-swiper", {
        direction: 'horizontal',
        slidesPerView: 6,
        spaceBetween: 6,
        breakpoints: {
          900: {
            direction: 'vertical',
            spaceBetween: 6,
          },
        },
      });
      var swiper2 = new Swiper(".large-swiper", {
        spaceBetween: 48,
        effect: 'fade',
        slidesPerView: 1,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        thumbs: {
          swiper: swiper,
        },
      });

    }

    // product single page
    var thumb_slider = new Swiper(".product-thumbnail-slider", {
      slidesPerView: 5,
      spaceBetween: 10,
      // autoplay: true,
      direction: "vertical",
      breakpoints: {
        0: {
          direction: "horizontal"
        },
        992: {
          direction: "vertical"
        },
      },
    });

    // product large
    var large_slider = new Swiper(".product-large-slider", {
      slidesPerView: 1,
      // autoplay: true,
      spaceBetween: 0,
      effect: 'fade',
      thumbs: {
        swiper: thumb_slider,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    

  }); // End of a document

})(jQuery);