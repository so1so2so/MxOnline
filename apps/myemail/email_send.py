#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from  MxOnline.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        # random.randint(0, length) 生成这个字符串的0开始到结束的下标 在取这个字符串的哪一个
        str+=chars[random.randint(0, length)]
    return str

def mysend_email(email ,type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    # 邮箱表的code字段等于新函数random_str创建的code
    email_record.code = code
    email_record.send_type =type
    email_record.email=email
    email_record.save()
    # 发送邮件
    email_title = "标题"
    email_body = "内容"
    if type == 'register':
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活账户:http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email],)
        if send_status:
            pass

    elif type == 'forget':
        email_title = "重置链接"
        email_body = "请点击下面的链接重置:http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email],)
        if send_status:
            pass