from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.jwt_ayth import create_token


class LoginView(APIView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        """
        用户登录
        """
        user = request.data.get('username')
        pwd = request.data.get('password')
        print(user, pwd)
        if user == 'Lone' and pwd == '123':
            token = create_token({'username': user})
            return Response({'status': True, 'token': token})
        return Response({'status': False, 'error': '用户名或密码错误'})


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response(request.user)

