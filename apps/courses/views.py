# !/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
# Create your views here.
# 分页函数
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course,CourseResource
from operation.models import UserFavorite
from operation.models import UserCourse,CourseComments
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


class CourseInfoView(View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course":course,
            "course_resources":all_resources,
            "relate_courses":relate_courses
        })

class CommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all().order_by("-id")
        return render(request, "course-comment.html", {
            "course":course,
            "course_resources":all_resources,
            "all_comments":all_comments

        })


class AddComentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id >0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')