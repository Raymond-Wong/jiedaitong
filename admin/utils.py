# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import date

'''
判断keys中的关键字是否都在data中存在
'''
def check_data_complete(data, keys):
  for key in keys:
    if data.get(key, None) is None:
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