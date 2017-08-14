# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from .models import Blog
from django.http import Http404
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, LoginForm


def index(request):
    post_list = Blog.objects.all()
    return render(request, 'index.html', {'post_list': post_list})


@csrf_exempt
def register(request):
    if request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']
            if User.objects.filter(username=username):
                return HttpResponse('<h1>此用户名已被注册</h1>')
            else:
                user = User.objects.create_user(username, email, password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                user = authenticate(username=username, password=password)
                auth.login(request, user)
                return render(request, 'index.html')
        else:
            return render(request, 'failure.html', {'reason': user_form.errors})
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'form': user_form})


@csrf_exempt
def login(request):
    form = LoginForm()
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if User.objects.filter(username=username):
                if user is not None:
                    auth.login(request, user)
                    response = render(request, 'index.html', {'form': login_form})
                    # 将username写入浏览器cookie,失效时间为3600
                    response.set_cookie('username', username, 3600)
                    return response
            else:
                # 比较失败，还在login
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return render(request, 'index.html', locals())


def detail(request):
    try:
        post = Blog.objects.get(id=str(id))
    except Blog.DoesNotExist:
        raise Http404
    return render(request, post.html, {'post': post})
