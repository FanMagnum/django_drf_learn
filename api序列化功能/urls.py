#!/usr/bin/env python
# encoding: utf-8
"""
@author: Lone
@email: fanml@neusoft.com
@file: urls.py
@time: 2020/5/20 13:35
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('books/', views.BookAPIView.as_view()),
    path('books/<int:pk>/', views.BookAPIView.as_view()),
]