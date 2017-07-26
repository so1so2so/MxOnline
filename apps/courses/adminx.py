#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.contrib import admin

# Register your models here.
import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse


class CourseAdmin(object):
    list_display = ['name', 'detail', 'degree']
    search_fields = ['name', 'detail', 'degree']
    list_filter = ['name', 'detail', 'degree']


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']


class LessonAdmin(object):
    list_display = ['course', 'name', 'learn_times']
    search_fields = ['course', 'name', 'learn_times']
    list_filter = ['course__name', 'name', 'learn_times']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
