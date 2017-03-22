var post = function(url, data, callback) {
  $.ajax({
    url : url,
    data : data,
    type : 'POST',
    success : callback,
    error: function() {
      alert('系统升级中，请求失败');
    }
  });
}

var select_with_name = function(name, selector) {
  if (selector == undefined) return $('input[name="' + name + '"]');
  return $(selector + '[name="' + name + '"]');
}