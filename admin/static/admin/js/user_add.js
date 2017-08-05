$(document).ready(function() {
  $('#submit_btn').click(function() {
    var params = {};
    params['name'] = $('input[name="name"]').val();
    params['phone'] = $('input[name="phone"]').val();
    params['address'] = $('input[name="address"]').val();
    params['certificate_type'] = $('select[name="certificate_type"]').val();
    params['certificate_num'] = $('input[name="certificate_num"]').val();
    post('/admin/user/add', params, function(resp) {
      alert(resp['msg']);
      if (resp['code'] == 0) {
        window.location.href = '/admin/user/list';
      }
    });
  });
});