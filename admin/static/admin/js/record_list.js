$(document).ready(function() {
  $('tr.record').click(function() {
    var rid = $(this).attr('rid');
    window.location.href = '/admin/record/get?rid=' + rid;
  });
});