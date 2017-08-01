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
from .views import CourseListView,CourseDetaiView, CourseInfoView, CommentsView, AddComentsView
urlpatterns = [
      url(r'^list/$', CourseListView.as_view(), name='course_list'),
      url(r'^detail/(?P<org_id>\d+)$', CourseDetaiView.as_view(), name='course_detail'),
      # 课程详情
      url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

        # 课程评论
      url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comments"),

        # 添加课程评论
      url(r'^add_comment/$', AddComentsView.as_view(), name="add_comment")

]
