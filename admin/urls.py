from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.record_list, name='record_list'),
  url(r'test', views.test, name='test'),
  url(r'record/list', views.record_list, name='record_list'),
  url(r'record/add', views.record_add, name='record_add'),
  url(r'record/delete', views.record_delete, name='record_delete'),
  url(r'record/repay/add', views.repay_record_add, name='repay_record_add'),
  url(r'record/repay/update', views.repay_record_update, name='repay_record_update'),
  url(r'record/get', views.record_get, name='record_get'),
  url(r'user/add', views.user_add, name='user_add'),
  url(r'user/list', views.user_list, name='user_list'),
  url(r'user/delete', views.user_delete, name='user_delete'),
  url(r'login', views.login, name='login'),
  url(r'logout', views.logout, name='logout'),
)
