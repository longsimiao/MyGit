# -*- coding:utf-8 -*-
import sys
import os
from django.conf import settings

BASE_DIR = os.path.dirname(__file__)
# DEBUG = os.environ.get('DEBUG', 'on') == 'on'
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
SECRET_KEY = os.environ.get('SECRET_KEY', '{{ SECRET_KEY }}')

settings.configure(
    DEBUG=True,
    SECRET_KEY=SECRET_KEY,
    # ALLOWED_HOSTS=ALLOWED_HOSTS,
    # ALLOWED_HOSTS=['localhost', '127.0.0.1', '[::1]', '0.0.0.0'],
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASS=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'sitebuilder',
        'compressor',
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ),
    STATIC_URL='/static/',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
    # 一旦命令完成后生成的静态文件存放目录
    SITE_OUTPUT_DIRECTORY=os.path.join(BASE_DIR, '_build'),
    # 启用在_build目录下的静态内容
    STATIC_ROOT=os.path.join(BASE_DIR, '_build', 'static'),
    STATICFILES_FINDERS=(
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    ),
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage',
)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
