from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    date_time = models.DateField(auto_now_add=True)
    modify_time = models.DateTimeField('Last Modified', auto_now=True)
    # content = models.TextField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']




