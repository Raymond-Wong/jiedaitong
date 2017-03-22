# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import json

class Response:
  def __init__(self, c=0, m=""):
    self.code = c
    self.msg = m
  def toJson(self):
    tmp = {}
    tmp["code"] = self.code
    tmp["msg"] = self.msg
    return json.dumps(tmp, ensure_ascii=False)