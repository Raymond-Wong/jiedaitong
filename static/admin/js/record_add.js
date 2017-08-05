$(document).ready(function() {
  $('#submit_btn').click(function() {
    var params = {};
    params['borrower_name'] = select_with_name('borrower_name').val();
    params['borrower_certificate_num'] = select_with_name('borrower_certificate_num').val();
    params['guarantor_name'] = select_with_name('guarantor_name').val();
    params['guarantor_certificate_num'] = select_with_name('guarantor_certificate_num').val();
    params['guarantee'] = select_with_name('guarantee').val();
    params['money'] = select_with_name('money').val();
    params['month_interest_rate'] = select_with_name('month_interest_rate').val();
    params['borrow_date'] = select_with_name('borrow_date').val();
    params['repay_date'] = select_with_name('repay_date').val();
    params['repay_interest_day'] = select_with_name('repay_interest_day').val();
    post('/admin/record/add', params, function(resp) {
      alert(resp['msg']);
      if (resp['code'] == 0) {
        window.location.href = '/admin/record/list';
      }
    });
  });
});