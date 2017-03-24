$(document).ready(function() {
  get_record_list_action();
  save_repay_record_action();
});

var get_record_list_action = function() {
  var select = $('select');
  $('td.btn').click(function() {
    var certificate_num = select_with_name('certificate_num').val();
    post('/admin/record/list', {'certificate_num' : certificate_num}, function(resp) {
      if (resp['code'] != 0) {
        alert(resp['msg']);
        return false;
      }
      select.html('');
      var records = $.parseJSON(resp['msg']);
      for (var i = 0; i < records.length; i++) {
        var record = records[i]['fields'];
        var rid = records[i]['pk'];
        var record_str = record['borrow_date'] + ' 至 ' + record['repay_date'];
        select.append('<option value="' + rid +'">' + record_str + '</option>');
      }
    });
  });
}

var save_repay_record_action = function() {
  $('#submit_btn').click(function() {
    var params = {};
    params['name'] = select_with_name('name').val();
    params['certificate_num'] = select_with_name('certificate_num').val();
    params['rid'] = $('select').val();
    params['repay_date'] = select_with_name('repay_date').val();
    params['money'] = select_with_name('repay_money').val();
    post('/admin/record/repay/add', params, function(resp) {
      alert(resp['msg']);
      if (resp['code'] == 0) {
        window.location.href = '/admin/record/list';
      }
    });
  });
}