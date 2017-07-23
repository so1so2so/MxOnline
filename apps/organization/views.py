#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from models import *


# Create your views here.
class OrgView(View):
    '''
    课程机构列表功能
    '''

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_city = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 赛选类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        org_num = all_orgs.count()
        sort = request.GET.get('sort', '')
        if sort:
            if sort=="students":
                all_orgs = all_orgs.order_by("-students")
            elif sort=="courses":
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
                'category':category,
                'hot_orgs':hot_orgs,
                'sort':sort
            })
