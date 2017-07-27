#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response
from forms import AnotherUserAskForm
# 分页函数
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from models import *
from operation.models import UserFavorite
from courses import *
from django.http import HttpResponse
import json
from users.models import UserProfile
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
        a = request.path
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'a':a
        })


class AddUserAskView(View):
    """
    用户添加咨询
   """

    def post(self, request):
        ret = {'status': 'success'}
        err = {'status': 'fail', 'msg': '你填写的信息有错,请检查'}
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

    def get(self, request, org_id):
        current = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 是否收藏
        has_fav =False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=course_org.id,fav_type=2):
                has_fav =True
        user = UserProfile.objects.name
        # 反向调用
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current': current,
            'user':user,
            'has_fav':has_fav,
        })


class TestView(View):
    def get(self, requesr):
        return render(requesr, 'org_base.html', {"msg": 'faule'})


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav =False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=course_org.id,fav_type=2):
                has_fav =True
        # 反向调用
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current': current,
            'has_fav':has_fav,
        })


class OrgDescView(View):
    """
    机构详情列表页
    """

    def get(self, request, org_id):
        current = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav =False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=course_org.id,fav_type=2):
                has_fav =True
        # 反向调用
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-desc.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current': current,
            'has_fav':has_fav,
        })


class OrgTeachersView(View):
    """
    机构教师列表页
    """

    def get(self, request, org_id):
        current = 'teachers'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav =False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=course_org.id,fav_type=2):
                has_fav =True
        # 反向调用
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current': current,
            'has_fav':has_fav,
        })


class AddFavView(View):
    """
    用户收藏及取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id')
        fav_id = int(fav_id)
        fav_type = request.POST.get('fav_type')
        fav_type=int(fav_type)
        # 判断用户登录状态
        if not request.user.is_authenticated():
            message = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(message))
        exist_records = UserFavorite.objects.filter(user=request.user,
                                                    fav_id=fav_id,
                                                    fav_type=fav_type)
        if exist_records:
            # 如果已经存在,表示用户取消收藏
            exist_records.delete()
            message = {"status":"success", "msg":"未收藏"}
            return HttpResponse(json.dumps(message))
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type > 0:
                user = request.user
                user_fav.user = user

                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                print type(fav_type),type(fav_id),type(user)
                user_fav.save()
                message = {"status":"success", "msg":"已收藏"}
                return HttpResponse(json.dumps(message))
            else:
                message = {"status":"fail", "msg":"收藏出错"}
                return HttpResponse(json.dumps(message))
