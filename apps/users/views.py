#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login as login2
from django.contrib.auth.backends import ModelBackend
from models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm
from django.contrib.auth.hashers import make_password
# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            pwd = request.POST.get('password')
            use = authenticate(username=username, password=pwd)
            if use is not None:
                login2(request, use)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('username')
            pwd = request.POST.get('password')
            user_writ = UserProfile()
            user_writ.username= username
            user_writ.email=username
            user_writ.password=make_password(pwd)
            user_writ.save()










































class CustonBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        use = authenticate(username=username, password=pwd)
        print use
        if use is not None:
            login2(request, use)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': '用户名或者密码错误'})
    elif request.method == 'GET':
        print 'get'
        return render(request, 'login.html')
