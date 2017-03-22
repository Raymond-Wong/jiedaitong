# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from django.http import HttpResponseRedirect

def is_logined(view):
  def logined(request, *args, **kwargs):
    print request.session.get('user', None)
    if request.session.get('user', None) is not None:
      return view(request, *args, **kwargs)
    else:
      return HttpResponseRedirect('/admin/login')
  return logined