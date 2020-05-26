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
    path('v1/books/', views.BookMixinGenericAPIView.as_view()),
    path('v1/books/<int:pk>/', views.BookMixinGenericAPIView.as_view()),
    path('v2/books/', views.BookListCreateAPIView.as_view()),
    path('v2/books/<int:pk>/', views.BookListCreateAPIView.as_view()),
]