# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from datetime import date, datetime, timedelta

'''
判断keys中的关键字是否都在data中存在
'''
def check_data_complete(data, keys):
  for key in keys:
    if data.get(key, None) is None or data.get(key, '').strip() == '':
      return False, key
  return True, None

'''
判断数据类型是否正确
'''
def check_data_type(data, keys):
  for key in keys:
    val = data.get(key[0])
    if not isinstance(val, key[1]):
      try:
        key[1](val)
        continue
      except:
        return False, key
  return True, None

'''
根据yyyy-mm-dd的形式创建date实例
'''
def create_date_by_str(date_str):
  year, month, day = date_str.split('-')
  try:
    year = int(year)
    month = int(month)
    day = int(day)
    return date(year, month, day)
  except Exception as e:
    return None

'''
将record的某些属性修改至用于展示
'''
def parse_record(record):
  record.money /= 100.0
  record.month_interest_rate *= 100.0
  record.repaid_interest /= 100.0
  record.repaid_money /= 100.0
  return record

'''
将django对象转换成字典
'''
def object_to_dict(obj):
  return dict([(attr, getattr(obj, attr)) for attr in [f.name for f in obj._meta.fields]])

'''
处理包含datetime字段的字典的json encoder
'''
class JSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
      return obj.strftime('%Y-%m-%d')
    else:
      return json.JSONEncoder.default(self, obj)

'''
判断当前日期是否是当前月份的最后一天
'''
def is_last_day(day):
  next_day = day + timedelta(days=1)
  return next_day.month != day.month


