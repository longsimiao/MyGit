# -*- coding:utf-8 -*-
import os
import json

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader_tags import BlockNode
from django.utils._os import safe_join


def get_page_or_404(name):
    try:
        # 使用safe_join将页面文件路径和模板文件名连接起来
        # 并返回规范化的最终的绝对路径
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page Not Found')
    # 打开每个文件并使用文件内容创建新的Django模板
    with open(file_path, 'r') as f:
        page = Template(f.read())

    meta = None
    for i, node in enumerate(list(page.nodelist)):
        if isinstance(node, BlockNode) and node.name == 'context':
            meta = page.nodelist.pop(i)
            break
    page._meta = meta
    return page


def page(request, slug='index'):
    # 将要修饰的page和slug上下文传递给page.html布局模板
    file_name = '{}.html'.format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': page,
    }
    if page._meta is not None:
        meta = page._meta.render(Context())
        extra_context = json.loads(meta)
        context.update(extra_context)
    return render(request, 'page.html', context)
