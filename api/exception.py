#!/usr/bin/env python
# encoding: utf-8
"""
@author: Lone
@email: fanml@neusoft.com
@file: exception.py
@time: 2020/5/20 18:08
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


# 自动以处理异常函数
def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        print(f"{context['view']} - {context['request'].method} - {exc}")
        return Response(
            {
                'detail': 'server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True
        )
    return response
