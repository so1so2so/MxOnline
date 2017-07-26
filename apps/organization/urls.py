# !/usr/bin/env python
# _*_ coding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgHomeView,TestView,OrgCourseView,OrgDescView,OrgTeachersView,AddFavView
urlpatterns = [
      url(r'^list.html/$', OrgView.as_view(), name='org_list'),
      url(r'^test.html/$', TestView.as_view(), name='test'),
      url(r'^add.html/$', AddUserAskView.as_view(), name='add'),
      url(r'^home.html/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
      url(r'^course.html/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
      url(r'^desc.html/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
      url(r'^teachers.html/(?P<org_id>\d+)/$', OrgTeachersView.as_view(), name='org_teachers'),
      url(r'^add_fav/$', AddFavView.as_view(), name='org_add_fav'),
]
