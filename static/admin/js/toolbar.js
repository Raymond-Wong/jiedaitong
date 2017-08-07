$(document).ready(function() {
  show_second_order_menu_action();
  close_all_menu_action();
});

var show_second_order_menu_action = function() {
  $(document).delegate('.first_order_menu', 'click', function() {
    var btn = $(this);
    var second_box = btn.children('.second_order_menu_box');
    var second_menu = second_box.children('.second_order_menu');
    if (second_menu.length > 0) {
      if (second_box.css('display') == 'none') {
        second_box.show();
      } else {
        second_box.hide();
      }
    }
    return false;
  })
}

var close_all_menu_action = function() {
  $(window).click(function() {
    $('.second_order_menu_box').hide();
  });
}