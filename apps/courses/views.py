# !/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
# 分页函数
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 6, request=request)
        orgs = p.page(page)
        return render(request, 'course-list.html',{
            'all_course': orgs
        })