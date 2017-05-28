# -*- coding: utf-8 -*-
"""
Chapter 1
@ Example 2
@ python example_02.py runserver
@ Browser: 127.0.0.1:8000 or localhost:8000
"""
import os
import sys
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application


DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '{{ SECRET_KEY }}')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    # SECRET_KEY生产环境中不使用。必须要生成用于默认会话和跨站点请求防伪(CSRF)保护密钥
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ),
)


def index(request):
    return HttpResponse('Hello world! This is example 2 project.')

urlpatterns = (
    url(r'^$', index),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
