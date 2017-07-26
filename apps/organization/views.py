#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response
from forms import AnotherUserAskForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from models import *
from courses import *
from django.http import HttpResponse


# Create your views here.
class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_city = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 赛选类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        org_num = all_orgs.count()
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
   """

    def post(self, request):
        ret = {'status': 'success'}
        err = {'status':'fail','msg':'你填写的信息有错,请检查'}
        import json
        userask_form = AnotherUserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save()
            return HttpResponse(json.dumps(ret))
        else:
            A = userask_form.errors
            print A
            # err = {'status':'fail','msg':userask_form.errors.as_json
            return HttpResponse(json.dumps(err))


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向调用
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current':current,
        })
class TestView(View):
    def get(self,requesr):
        return render(requesr,'org_base.html',{"msg":'faule'})
class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向调用
        all_courses = course_org.course_set.all()

        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current':current,
        })
class OrgDescView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向调用
        all_courses = course_org.course_set.all()

        return render(request,'org-detail-desc.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current':current,
        })
class OrgTeachersView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current = 'teachers'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向调用
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request,'org-detail-teachers.html',{
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current':current,
        })