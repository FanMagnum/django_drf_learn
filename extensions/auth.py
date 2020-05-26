#!/usr/bin/env python
# encoding: utf-8
"""
@author: Lone
@email: fanml@neusoft.com
@file: auth.py
@time: 2020/5/26 10:34
"""
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from utils.jwt_ayth import parse_payload


class JwtQueryParamAuthentication(BaseAuthentication):
    """
    用户需要在url中通过参数进行token传输，例如：
    token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def authenticate(self, request):
        token = request.query_params.get('token')
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (payload, token)


class JwtAuthorizationAuthentication(BaseAuthentication):
    """
    用户需要通过请求头的方式来进行传输token
    """
    def authenticate(self, request):
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        if not authorization:
            raise exceptions.AuthenticationFailed({'error': '未获取到Authorization请求头', 'status': False})
        token = authorization
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)
        return (payload, token)