#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # captcha = CaptchaField(error_messages={'invalid': u'你的验证码错误,请检查'})
    captcha = CaptchaField(error_messages={"invalid":u"你的,验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"你的,验证码错误"})


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)