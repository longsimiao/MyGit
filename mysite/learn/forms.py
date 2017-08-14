#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 8/14/17 2:19 AM
# @Author  : Ferras
# @Email   : mxlmiao@sina.cn
# @File    : forms.py
# @Software: PyCharm
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    email = forms.EmailField(max_length=50, widget=forms.TextInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
