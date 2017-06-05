# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog
from django.http import Http404


def index(request):
    post_list = Blog.objects.all()
    return render(request, 'index.html', {'post_list': post_list})


def detail(request):
    try:
        post = Blog.objects.get(id=str(id))
    except Blog.DoesNotExist:
        raise Http404
    return render(request, post.html, {'post': post})
