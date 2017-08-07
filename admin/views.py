# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import jiedaitong.models
import utils
from jiedaitong.utils import Response

from jiedaitong.decorators import is_logined

def test(request):
  return render(request, 'admin/widgets/base.html')

@csrf_exempt
def login(request):
  if request.method == 'GET':
    return render(request, 'admin/login.html')
  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  if username == 'admin' and password == 'admin':
    request.session['user'] = 0
    return HttpResponse(Response(c=0, m='登陆成功').toJson(), content_type="application/json")
  return HttpResponse(Response(c=1, m='请输入正确的账号和密码').toJson(), content_type='application/json')

@is_logined
def logout(request):
  del request.session['user']
  return HttpResponseRedirect('/admin/login')

@csrf_exempt
@is_logined
def record_list(request):
  if request.method == 'GET':
    raise Http404
  start = int(request.POST.get('start', '0'))
  num = request.POST.get('num', 'all')
  records = jiedaitong.models.Record.objects.all().order_by('create_time')
  if num == 'all':
    records = records[start:]
  else:
    records = records[start:start + int(num)]
  dict_records = []
  for ridx, record in enumerate(records):
    dict_record = utils.object_to_dict(record)
    dict_record['money'] /= 100.0
    dict_record['month_interest'] = dict_record['money'] * record.month_interest_rate
    dict_record['repaid_interest'] /= 100.0
    dict_record['month_interest_rate'] *= 100.0
    dict_record['repaid_interest_month'] = record.repay_record_set.count()
    dict_record['user'] = dict(name=record.user.name, phone=record.user.phone)
    dict_record['guarantor'] = None
    dict_records.append(dict_record)
  records = json.dumps(dict_records, cls=utils.JSONEncoder)
  return HttpResponse(Response(m=records).toJson(), content_type="application/json")

@csrf_exempt
@is_logined
def record_add(request):
  if request.method == 'GET':
    raise Http404
    # return render(request, 'admin/record_add.html', {'page' : 'record_add', 'wf_title' : '添加贷款记录'})
  # 判断数据完备性
  data_complete, missing_data = utils.check_data_complete(request.POST, ['borrower_name', 'borrower_certificate_num', 'guarantor_name', 'guarantor_certificate_num', 'guarantee', 'money', 'month_interest_rate', 'borrow_date', 'repay_date', 'repay_interest_day'])
  if not data_complete:
    return HttpResponse(Response(c=-1, m='未提供参数：%s' % missing_data).toJson(), content_type="application/json")
  data_type_right, wrong_type = utils.check_data_type(request.POST, [('money', float), ('month_interest_rate', float), ('repay_interest_day', int)])
  if not data_type_right:
    return HttpResponse(Response(c=-2, m='%s必须为%s类型' % wrong_type).toJson(), content_type="application/json")
  # 判断借款人是否存在
  if jiedaitong.models.User.objects.filter(name=request.POST.get('borrower_name')).filter(certificate_num=request.POST.get('borrower_certificate_num')).count() <= 0:
    return HttpResponse(Response(c=1, m='系统中无法查询到借款人，请确认是否已添加借款人').toJson(), content_type="application/json")
  # 判断担保人是否存在
  if jiedaitong.models.User.objects.filter(name=request.POST.get('guarantor_name')).filter(certificate_num=request.POST.get('guarantor_certificate_num')).count() <= 0:
    return HttpResponse(Response(c=2, m='系统中无法查询到担保人，请确认是否已添加担保人').toJson(), content_type="application/json")
  borrower = jiedaitong.models.User.objects.filter(name=request.POST.get('borrower_name')).filter(certificate_num=request.POST.get('borrower_certificate_num'))[0]
  guarantor = jiedaitong.models.User.objects.filter(name=request.POST.get('guarantor_name')).filter(certificate_num=request.POST.get('guarantor_certificate_num'))[0]
  # 判断金额是否合法
  money = float(request.POST.get('money')) * 100.0
  if money <= 0:
    return HttpResponse(Response(c=3, m='借款金额不得小于0').toJson(), content_type="application/json")
  # 判断月利息是否合法
  month_interest_rate = float(request.POST.get('month_interest_rate')) / 100.0
  if month_interest_rate <= 0:
    return HttpResponse(Response(c=4, m='月利息必须大于0').toJson(), content_type="application/json")
  # 判断借款日期是否合法
  borrow_date = utils.create_date_by_str(request.POST.get('borrow_date'))
  if borrow_date is None:
    return HttpResponse(Response(c=5, m='借款日期有误').toJson(), content_type="application/json")
  repay_date = utils.create_date_by_str(request.POST.get('repay_date'))
  if repay_date is None:
    return HttpResponse(Response(c=6, m='还款日期有误').toJson(), content_type="application/json")
  # 判断还款日期要大于借款日期
  if repay_date < borrow_date:
    return HttpResponse(Response(c=7, m='借款日期必须早于还款日期').toJson(), content_type="application/json")
  # 判断每月还款日期是否合法
  repay_interest_day = int(request.POST.get('repay_interest_day'))
  if repay_interest_day < 1 or repay_interest_day > 31:
    return HttpResponse(Response(c=8, m='每月还款日期必须大于0，小于等于31').toJson(), content_type="application/json")
  jiedaitong.models.Record(user=borrower, guarantor=guarantor, guarantee=request.POST.get('guarantee'), money=money, month_interest_rate=month_interest_rate, repay_interest_day=repay_interest_day, borrow_date=borrow_date, repay_date=repay_date).save()
  return HttpResponse(Response(c=0, m='创建借贷记录成功').toJson(), content_type='application/json')

@csrf_exempt
@is_logined
def record_delete(request):
  if request.method == 'GET':
    raise Http404
  rid = request.POST.get('id', '0')
  record = jiedaitong.models.Record.objects.filter(id=rid)
  if record.count() <= 0:
    return HttpResponse(Response(c=1, m='待删除记录不存在！').toJson(), content_type="application/json")
  record = record[0]
  record.delete()
  return HttpResponse(Response(c=0, m='删除成功！').toJson(), content_type="application/json")

@csrf_exempt
@is_logined
def record_get(request):
  if request.method == 'GET':
    raise Http404
  data_complete, missing_data = utils.check_data_complete(request.POST, ['rid'])
  if not data_complete:
    raise Http404
  data_type_right, wrong_type = utils.check_data_type(request.POST, [('rid', int)])
  if not data_type_right:
    raise Http404
  if jiedaitong.models.Record.objects.filter(id=int(request.POST.get('rid'))).count() <= 0:
    raise Http404
  record = jiedaitong.models.Record.objects.get(id=int(request.POST.get('rid')))
  record = utils.parse_record(record)
  dict_record = utils.object_to_dict(record)
  dict_record['user'] = utils.object_to_dict(record.user)
  dict_record['guarantor'] = utils.object_to_dict(record.guarantor)
  dict_record['month_interest'] = record.money * record.month_interest_rate / 100.0
  record = json.dumps(dict_record, cls=utils.JSONEncoder)
  return HttpResponse(Response(c=0, m=record).toJson(), content_type="application/json")

@csrf_exempt
@is_logined
def repay_record_add(request):
  if request.method == 'GET':
    raise Http404
    # return render(request, 'admin/repay_record_add.html', {'page' : 'repay_record_add'})
  data_complete, missing_data = utils.check_data_complete(request.POST, ['name', 'certificate_num', 'rid', 'repay_date', 'money'])
  if not data_complete:
    return HttpResponse(Response(c=-1, m='未提供参数：%s' % missing_data).toJson(), content_type="application/json")
  data_type_right, wrong_type = utils.check_data_type(request.POST, [('money', float), ('rid', int)])
  if not data_type_right:
    return HttpResponse(Response(c=-2, m='%s必须为%s类型' % wrong_type).toJson(), content_type="application/json")
  name = request.POST.get('name')
  certificate_num = request.POST.get('certificate_num')
  rid = int(request.POST.get('rid'))
  repay_date = utils.create_date_by_str(request.POST.get('repay_date'))
  money = float(request.POST.get('money')) * 100
  # 获取用户
  users = jiedaitong.models.User.objects.filter(certificate_num=certificate_num)
  if users.count() <= 0:
    return HttpResponse(Response(c=1, m='用户不存在').toJson(), content_type='application/json')
  user = users[0]
  # 获取借款记录
  records = jiedaitong.models.Record.objects.filter(id=rid)
  if records.count() <= 0:
    return HttpResponse(Response(c=2, m='借款记录不存在').toJson(), content_type="application/json")
  record = records[0]
  # 判断借款记录是否属于同一个用户
  if record.user != user:
    return HttpResponse(Response(c=3, m='借款记录不属于当前用户').toJson(), content_type="application/json")
  jiedaitong.models.Repay_Record(user=user, record=record, repay_date=repay_date, money=money).save()
  record.repaid_interest += money
  record.save()
  return HttpResponse(Response(m='添加还息记录成功').toJson(), content_type="application/json")

@csrf_exempt
def repay_record_update(request):
  today = timezone.make_naive(timezone.now(), timezone.get_current_timezone()).date()
  records = jiedaitong.models.Record.objects.filter(state=1).filter(repay_date__gt=today)
  for record in records:
    if (record.repay_interest_day == today.day) or (utils.is_last_day(today) and utils.is_last_day(record.borrow_date)):
      money = record.month_interest_rate * record.money
      jiedaitong.models.Repay_Record(user=record.user, repay_date=today, record=record, money=money).save()
      record.repaid_interest += money
      record.save()
  print today, '更新了%d个借贷记录' % records.count()
  return HttpResponse('')

@csrf_exempt
@is_logined
def user_add(request):
  if request.method == 'GET':
    raise Http404
  # 判断数据完备性
  data_complete, missing_data = utils.check_data_complete(request.POST, ['name', 'phone', 'address', 'certificate_type', 'certificate_num'])
  if not data_complete:
    return HttpResponse(Response(c=-1, m='未提供参数：%s' % missing_data).toJson(), content_type="application/json")
  name = request.POST.get('name')
  phone = request.POST.get('phone')
  address = request.POST.get('address')
  certificate_type = request.POST.get('certificate_type')
  certificate_num = request.POST.get('certificate_num')
  # 检查数据类型
  data_type_right, wrong_type = utils.check_data_type(request.POST, [('certificate_type', int)])
  if not data_type_right:
    return HttpResponse(Response(c=-2, m='%s必须为%s类型' % wrong_type).toJson(), content_type="application/json")
  certificate_type = int(certificate_type)
  # 检查证件号是否重复
  if jiedaitong.models.User.objects.filter(certificate_type=certificate_type).filter(certificate_num=certificate_num).count() > 0:
    return HttpResponse(Response(c=1, m='每个用户的证件号必须唯一').toJson(), content_type="application/json")
  # 创建用户
  jiedaitong.models.User(name=name, phone=phone, address=address, certificate_type=certificate_type, certificate_num=certificate_num).save()
  return HttpResponse(Response(c=0, m='创建用户成功').toJson(), content_type="application/json")

@csrf_exempt
@is_logined
def user_delete(request):
  if request.method == 'GET':
    raise Http404
  uid = request.POST.get('id', '0')
  user = jiedaitong.models.User.objects.filter(id=uid)
  if user.count() <= 0:
    return HttpResponse(Response(c=1, m='待删除用户不存在！').toJson, content_type="application/json")
  user = user[0]
  print user.name
  user.delete()
  return HttpResponse(Response(c=0, m='删除成功！').toJson(), content_type="application/json")

@csrf_exempt
@is_logined
def user_list(request):
  if request.method == 'GET':
    raise Http404
  start = int(request.POST.get('start', '0'))
  num = request.POST.get('num', 'all')
  users = jiedaitong.models.User.objects.all().order_by('create_time')
  if num == 'all':
    users = users[start:]
  else:
    users = users[start:start + int(num)]
  dict_users = []
  for user in users:
    dict_users.append(utils.object_to_dict(user))
  users = json.dumps(dict_users, cls=utils.JSONEncoder)
  return HttpResponse(Response(c=0, m=users).toJson(), content_type="application/json")