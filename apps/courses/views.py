# !/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
# 分页函数
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course
from operation.models import UserFavorite
from operation.models import UserCourse

class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by("-add_time")
        # 课程排序
        sort = request.GET.get('sort')
        if sort:
            if sort=='students':
                all_course=all_course.order_by('-students')
            elif sort == 'hot':
                all_course=all_course.order_by('-click_nums')
        hot_orgs = all_course.order_by("-click_nums")[:3]
        # 课程分页
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
    def get(self, request, org_id):

        course = Course.objects.get(id=int(org_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()
        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False
        # 判断用户登录
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_coures = Course.objects.filter(tag=tag)[:3]
        else:
            relate_coures = []
        return render(request, 'course-detai.html',{
            'course': course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
            'relate_coures':relate_coures,
        })