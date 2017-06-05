from __future__ import unicode_literals

from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    date_time = models.DateField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']




