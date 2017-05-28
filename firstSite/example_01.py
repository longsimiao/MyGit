# -*- coding: utf-8 -*-
"""
Chapter 1
@ Example 1
@ python example_01.py runserver
@ Browser: 127.0.0.1:8000 or localhost:8000
"""
import sys
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url

settings.configure(
    DEBUG=True,
    # SECRET_KEY生产环境中不使用。必须要生成用于默认会话和跨站点请求防伪(CSRF)保护密钥
    SECRET_KEY='mxl123',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ),
)


def index(request):
    return HttpResponse('Hello world! This is example 1 project.')

urlpatterns = (
    url(r'^$', index),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

