from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
# 辅助GenericAPIView的工具
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin

from utils.response import APIResponse
from .models import Book
from .serializers import BookModelSerializer


class BookMixinGenericAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

    # 单查和群查
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            response = self.retrieve(request, *args, **kwargs)
        else:
            response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 单增
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(response.data)

    # 单整体修改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(response.data)

    # 单局部修改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(response.data)


# 工具视图
# 1）工具视图都是GenericAPIView的子类，且不同的子类继承了不同的工具类
# 2）工具视图的功能可以满足需求，只需要继承工具视图，并且提供queryset与serializer_class即可
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView


class BookListCreateAPIView(ListCreateAPIView, UpdateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
