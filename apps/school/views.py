# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import traceback

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.school.serializers import Work, WorkSerializer
from lib.restful import ClientParamsInvalidError, SUCCESS, FAILURE
# Create your views here.


class WorkList(GenericAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    ordering = ('id',)
    filter_fields = '__all__'

    def get(self, request, format=None):
        res = {'result': {}, 'msg': '', 'code': SUCCESS}
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res['result'] = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                res['result'] = serializer.data
        except ClientParamsInvalidError as e:
            res['msg'] = getattr(e, 'msg')
            res['code'] = getattr(e, 'code')
        except Exception as e:
            res['msg'] = '内部服务错误'
            res['code'] = FAILURE.serverError
            traceback.print_exc()
        finally:
            return Response(res)
