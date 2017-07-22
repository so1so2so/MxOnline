#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, login as login2
from django.contrib.auth.backends import ModelBackend
from models import UserProfile,EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetForm,ChangePasswordForm
from django.contrib.auth.hashers import make_password
# Create your views here.
from myemail.email_send import mysend_email

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
                if use.is_active:
                    login2(request, use)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ActiveUser(View):
    def get(self,request,active_code):
        all_code = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code:
            # print all_code.email
            for i in all_code:
                email=i.email
                user = UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
                return HttpResponse('<h1>用户激活成功<h1>')
        else:
            return HttpResponse('<p>链接失效<p>')



class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email')
            if UserProfile.objects.filter(username=username):
                return render(request, "register.html", {'msg': '用户已存在', 'register_form': register_form})
            else:
                pwd = request.POST.get('password')
                user_writ = UserProfile()
                user_writ.username= username
                user_writ.email=username
                user_writ.is_active =False
                user_writ.password=make_password(pwd)
                user_writ.save()
                mysend_email(username, 'register')
                return render(request, "login.html")
        else:
            return render(request, "register.html",{'register_form': register_form})


class ForGetView(View):
    '''
    发送邮件
    '''
    def get(self,request):
        pwd_form = ForgetForm()
        return render(request, "forgetpwd.html",{'pwd_form':pwd_form})

    def post(self,request):
        pwd_form = ForgetForm(request.POST)
        if pwd_form.is_valid():
            email = request.POST.get('email')
            mysend_email(email, 'forget')
            return HttpResponse('<p>邮件已发送,请查收</p>')
        else:
             return render(request, "forgetpwd.html",{'pwd_form':pwd_form})


class ResetUser(View):
    '''
    匹配链接并找到用户名称
    '''
    def get(self,request,reset_code):
        all_code = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_code:
            # print all_code.email
            for i in all_code:
                email=i.email
                return render(request, "password_reset.html",{'email': email})
        else:
            return HttpResponse('<p>链接失效<p>')
        return render(request,'login.html')


class changepwd(View):
    '''
    修改密码
    '''
    def post(self,request):
        change_pwd_form = ChangePasswordForm(request.POST)
        if change_pwd_form:
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            if pwd1==pwd2:
                user = UserProfile.objects.get(email=email)
                user.password=make_password(pwd1)
                user.save()
                return render(request,'login.html')
            else:
                return render(request, "password_reset.html",{'message': '2次密码不一致'})

        return render(request, "password_reset.html",{'change_pwd_form':change_pwd_form})































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
