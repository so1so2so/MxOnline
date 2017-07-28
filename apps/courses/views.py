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
        # 课程排序
        sort = request.GET.get('sort')
        if sort:
            if sort=='students':
                all_course=all_course.order_by('-students')
            elif sort == 'hot':
                all_course=all_course.order_by('-click_nums')
        hot_orgs = all_course.order_by("-click_nums")[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 6, request=request)
        orgs = p.page(page)
        a = request.path
        return render(request, 'course-list.html',{
            'all_course': orgs,
            'a':a,
            'sort':sort,
            'hot_orgs':hot_orgs

        })


class CourseDetaiView(View):
    def get(self, request,org_id):
        course = Course.objects.filter(id=int(org_id))
        # print all_user
        a = request.path
        return render(request, 'course-detai.html',{
            'all_course': course,
            'a':a,
            # 'all_user':all_user,
        })