from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models, serializers


class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 单查
        if pk:
            try:
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                book_data = serializers.BookModelSerializer(book_obj).data  # 序列化
            except:
                return Response({
                    'status': 1,
                    'msg': '参数有误'
                })
        # 群查
        else:
            book_query = models.Book.objects.filter(is_delete=False).all()
            book_data = serializers.BookModelSerializer(book_query, many=True).data  # 序列化

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': book_data
        })

    def post(self, request, *args, **kwargs):
        # 单增:传的数据是与model对应的一个字典
        # 群增：设计传递的是多个model对应的字典列表,在postman中通过列表嵌套字典传值
        request_data = request.data
        if isinstance(request_data, dict):  # 判断获取的数据是否是dict
            many = False
        elif isinstance(request_data, list):  # 判断获取的数据是否是list
            many = True
        else:
            return Response({
                'status': 1,
                'msg': '数据错误'
            })
        book_ser = serializers.BookModelSerializer(data=request_data, many=many)  # 反序列化
        book_ser.is_valid(raise_exception=True)
        book_result = book_ser.save()  # book_result是对象<class 'app01.models.Book'>，群增就是列表套一个个对象

        return Response(
            {
                'status': 0,
                'msg': 'ok',
                'results': serializers.BookModelSerializer(book_result, many=many).data
            }
        )

    # 单删: 有pk   #在postman中通过路径传参
    # 群删：有pks   {"pks": [1, 2, 3]}   #通过json传参
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if models.Book.objects.filter(pk__in=pks, is_delete=False).update(is_delete=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

    # 单整体改  对 v3/books/pk/  传的参数是与model对应的字典 {name|price|publish|authors}在json中传递
    def put(self, request, *args, **kwargs):
        request_data = request.data
        pk = kwargs.get('pk')
        # 先获取要修改的对象
        try:
            old_book_obj = models.Book.objects.get(pk=pk, is_delete=False)
        except:
            # 当输入不存在的pk
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        book_ser = serializers.BookModelSerializer(instance=old_book_obj, data=request_data, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookModelSerializer(book_obj).data
        })

    # 单局部改和群局部改整合
    # 单局部改：对 v3/books/pk/   pk通过路由传参，修改数据选择传参，通过数据包json传递
    # 群局部修改：v3/books/ 修改数据通过数据包传递，设置成列表格式  [{pk:1,name:123},{pk:3,price:7},{pk:7,publish:2}]
    def patch(self, request, *args, **kwargs):
        request_data = request.data  # 数据包数据
        pk = kwargs.get('pk')
        # 将单改，群改的数据都格式化成 pks=[要需要的对象主键标识] | request_data=[每个要修改的对象对应的修改数据]
        if pk and isinstance(request_data, dict):  # 单改
            pks = [pk, ]
            request_data = [request_data, ]
        elif not pk and isinstance(request_data, list):  # 群改
            pks = []
            # 遍历前台数据[{pk:1, name:123}, {pk:3, price:7}, {pk:7, publish:2}]，拿一个个字典
            for dic in request_data:
                pk = dic.pop('pk', None)  # 返回pk值
                if pk:
                    pks.append(pk)
                # pk没有传值
                else:
                    return Response({
                        'status': 1,
                        'msg': '参数错误'
                    })
        else:
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        # pks与request_data数据筛选，
        # 1）将pks中的没有对应数据的pk与数据已删除的pk移除，request_data对应索引位上的数据也移除
        # 2）将合理的pks转换为 objs
        objs = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                # 将pk合理的对象数据保存下来
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                objs.append(book_obj)
                # 对应索引的数据也保存下来
                new_request_data.append(request_data[index])
            except:
                # 重点：反面教程 - pk对应的数据有误，将对应索引的data中request_data中移除
                # 在for循环中不要使用删除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        # 生成一个serializer对象
        book_ser = serializers.BookModelSerializer(instance=objs, data=new_request_data, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_objs = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookModelSerializer(book_objs, many=True).data
        })
