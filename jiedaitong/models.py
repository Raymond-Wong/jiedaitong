# -*- coding: utf-8 -*-
from django.db import models

CERTIFICATION_TYPE = ((0, u'身份证'),)
class User(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  last_update_time = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=20)
  phone = models.CharField(max_length=20, default='')
  address = models.CharField(max_length=100, default='')
  certificate_type = models.PositiveIntegerField(choices=CERTIFICATION_TYPE, default=0)
  certificate_num = models.CharField(max_length=30, unique=True)

RECORD_STATE = ((0, u'未放款'), (1, u'已放款'), (2, u'已还清'))
class Record(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  last_update_time = models.DateTimeField(auto_now=True)
  state = models.PositiveIntegerField(default=1, choices=RECORD_STATE)
  user = models.ForeignKey(User)
  guarantor = models.ForeignKey(User, related_name='guarantee_records')
  guarantee = models.TextField()
  money = models.PositiveIntegerField(default=0)
  month_interest_rate = models.FloatField()
  repay_interest_day = models.PositiveIntegerField(default=1)
  repaid_interest = models.PositiveIntegerField(default=0)
  repaid_money = models.PositiveIntegerField(default=0)
  borrow_date = models.DateField()
  repay_date = models.DateField()

class Repay_Record(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  last_update_time = models.DateTimeField(auto_now=True)
  repay_date = models.DateField()
  user = models.ForeignKey(User)
  record = models.ForeignKey(Record)
  money = models.PositiveIntegerField()