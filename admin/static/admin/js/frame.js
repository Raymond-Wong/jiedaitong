$(document).ready(function() {
  max_win_action();
  min_win_action();
  close_win_action();
});

var max_win_action = function() {
  var is_max = false;
  var win = nw.Window.get();
  $('#max_win_btn').click(function() {
    if (!is_max) {
      win.maximize();
      is_max = true;
    } else {
      win.unmaximize();
      is_max = false;
    }
  });
}

var min_win_action = function() {
  var win = nw.Window.get();
  $('#min_win_btn').click(function() {
    win.minimize();
  });
}

var close_win_action = function() {
  $('#close_win_btn').click(function() {
    nw.App.quit();
  });
}