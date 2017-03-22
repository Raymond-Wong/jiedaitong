$(document).ready(function() {
  $('#login_btn').click(function() {
    var params = {};
    params['username'] = select_with_name('username').val();
    params['password'] = select_with_name('password').val();
    post('/admin/login', params, function(resp) {
      alert(resp['msg']);
      if (resp['code'] == 0) {
        window.location.href = '/admin/record/list'
      }
    });
  });
})