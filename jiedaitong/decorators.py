# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from django.http import HttpResponse
from utils import Response

def is_logined(view):
  def logined(request, *args, **kwargs):
    if request.session.get('user', None) is not None:
      return view(request, *args, **kwargs)
    else:
      return HttpResponse(Response(c=1001).toJson(), content_type="application/json")
  return logined