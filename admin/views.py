# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import jiedaitong.models
import utils
from jiedaitong.utils import Response

from jiedaitong.decorators import is_logined

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

@is_logined
def record_list(request):
  records = jiedaitong.models.Record.objects.all().order_by('create_time')
  for record in records:
    record.money /= 100.0
    record.repaid_interest /= 100.0
  return render(request, 'admin/record_list.html', {'page' : 'record_list', 'records' : records})

@csrf_exempt
@is_logined
def record_add(request):
  if request.method == 'GET':
    return render(request, 'admin/record_add.html', {'page' : 'record_add'})
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

@is_logined
def record_get(request):
  data_complete, missing_data = utils.check_data_complete(request.GET, ['rid'])
  if not data_complete:
    raise Http404
  data_type_right, wrong_type = utils.check_data_type(request.GET, [('rid', int)])
  if not data_type_right:
    raise Http404
  if jiedaitong.models.Record.objects.filter(id=int(request.GET.get('rid'))).count() <= 0:
    raise Http404
  record = jiedaitong.models.Record.objects.get(id=int(request.GET.get('rid')))
  record = utils.parse_record(record)
  record.month_interest = record.money * record.month_interest_rate / 100.0
  return render(request, 'admin/record_get.html', {'record' : record})

@csrf_exempt
@is_logined
def user_add(request):
  if request.method == 'GET':
    return render(request, 'admin/user_add.html', {'page' : 'user_add'})
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

@is_logined
def user_list(request):
  users = jiedaitong.models.User.objects.all().order_by('create_time')
  return render(request, 'admin/user_list.html', {'page' : 'user_list', 'users' : users})