#!/usr/bin/env python
# encoding: utf-8
"""
@author: Lone
@email: fanml@neusoft.com
@file: serializers.py
@time: 2020/5/21 14:38
"""
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, ListSerializer

from api import models


class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):  # print(instance)  # 要更新的对象们
        # print(validated_data)  # 更新的对象对应的数据们
        # print(self.child)  # 服务的模型序列化类 - V2BookModelSerializer
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializer(ModelSerializer):
    class Meta:
        list_serializer_class = BookListSerializer
        model = models.Book
        fields = ('name', 'price', 'publish', 'authors', 'author_list', 'publish_name')
        extra_kwargs = {
            'name': {
                'required': True,
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短',
                }
            },
            'publish': {
                'write_only': True
            },
            'authors': {
                'write_only': True
            },
            'author_list': {
                'read_only': True,
            },
            'publish_name': {
                'read_only': True,
            }
        }

    def validate_name(self, value):
        # 书名不能包含 g 字符
        if 'g' in value.lower():
            raise ValidationError('该g书不能出版')
        return value

    def validate(self, attrs):
        publish = attrs.get('publish')
        name = attrs.get('name')
        if models.Book.objects.filter(name=name, publish=publish):
            raise ValidationError({'book': '该书已存在'})
        return attrs
