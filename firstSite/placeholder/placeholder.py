# -*- coding: utf-8 -*-
"""
Chapter 2
@ Example 1
@ python example_01.py runserver
@ Browser: 127.0.0.1:8000 or localhost:8000
"""
import os
import sys
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django import forms
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.cache import cache


DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '')
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


class ImageForm(forms.Form):

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format="PNG"):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{} X {}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:

            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textwidth < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)
        return content


def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type="image/png")
    else:
        return HttpResponse('Invalid image request.')


def index(request):
    return HttpResponse('Hello world! This is example 2 project.')

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$', index, name='homepage'),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
