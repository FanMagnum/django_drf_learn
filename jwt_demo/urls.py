#!/usr/bin/env python
# encoding: utf-8
"""
@author: Lone
@email: fanml@neusoft.com
@file: urls.py
@time: 2020/5/26 10:14
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('order/', views.OrderView.as_view()),
]