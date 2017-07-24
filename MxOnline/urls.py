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
from django.views.generic import TemplateView
import xadmin
from users import views
from organization import urls
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('^login/$', views.LoginView.as_view(), name='login'),
    url('^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUser.as_view(), name='user_active'),
    url(r'^reset/(?P<reset_code>.*)/$', views.ResetUser.as_view(), name='reset'),
    url(r'^forget/$', views.ForGetView.as_view(), name='forget'),
    url(r'^changepwd/$', views.changepwd.as_view(), name='changepwd'),
    # url(r'^org-list.html/$', orgview.OrgView.as_view(), name='org_list'),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^org/', include('organization.urls', namespace='org')),
]
