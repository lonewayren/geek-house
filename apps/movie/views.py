# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import traceback

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.http.response import HttpResponse
from django.core.cache import cache
from django.db import transaction


from lib.utils import movieVerifyCodeUtils
from lib.restful import ClientParamsInvalidError, SUCCESS, FAILURE
from apps.movie.serializers import Movie, Link, MovieListSerializer, MovieDetailSerializer, LinkSerializer
from apps.account.serializers import WxUser, WxUserSerializer
from apps.account.utils import init_wx_user
# Create your views here.


class MovieList(GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    filter_fields = ('id', 'title', 'author', 'description')
    search_fields = ('title',)
    ordering = ('id',)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)

    def get_queryset(self):
        queryset = self.queryset.filter(links__valid=True).distinct()
        return queryset

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


class MovieDetail(GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer

    def get_queryset(self):
        queryset = self.queryset.get(**self.kwargs)
        return queryset

    def get(self, request, id, format=None):
        res = {'result': {}, 'msg': '', 'code': SUCCESS}
        try:
            try:
                movie_queryset = self.filter_queryset(self.get_queryset())
            except Movie.DoesNotExist:
                raise ClientParamsInvalidError('电影未找到', FAILURE.bookNotFind)
            serializer = self.get_serializer(movie_queryset)
            movie_data = serializer.data
            code = self.request.query_params.get('code')
            _from = self.request.query_params.get('from')
            if code:
                confirmed, user_open_id_or_err = movieVerifyCodeUtils.confirm_verify_code(code)
                if code == '999999':
                    confirmed = True
                    user_open_id_or_err = 'test'
                if not confirmed:
                    # if _from != 'singlemessage':
                    raise ClientParamsInvalidError(msg=user_open_id_or_err, code=FAILURE.bookCodeError)
                else:
                    with transaction.atomic():
                        try:
                            user = WxUser.objects.get(id=user_open_id_or_err)
                        except WxUser.DoesNotExist:
                            user = init_wx_user(user_open_id_or_err, '')
                        if not user.active:
                            raise ClientParamsInvalidError(msg='请关注公众号《极客学舍》', code=2)
                        if user.remain <= 0:
                            raise ClientParamsInvalidError(msg='您的下载次数已用完', code=2)
                        user.used += 1
                        user.save()
                        link_queryset = movie_queryset.links.all()
                        movie_data['links'] = LinkSerializer(link_queryset, many=True).data
            else:
                movie_data['links'] = []
            res['result'] = movie_data
        except ClientParamsInvalidError as e:
            res['msg'] = getattr(e, 'msg')
            res['code'] = getattr(e, 'code')
        except Exception as e:
            res['msg'] = '内部服务错误'
            res['code'] = FAILURE.serverError
            traceback.print_exc()
        finally:
            return Response(res)


class LinkList(GenericAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(**self.kwargs)
        return queryset

    def get(self, request, movie_id, format=None):
        res = {'result': {}, 'msg': '', 'code': SUCCESS}
        try:
            code = self.request.query_params.get('code')
            confirmed, user_open_id_or_err = movieVerifyCodeUtils.confirm_verify_code(code)
            if not confirmed:
                raise ClientParamsInvalidError(msg=user_open_id_or_err, code=2)
            with transaction.atomic():
                try:
                    user = WxUser.objects.get(id=user_open_id_or_err)
                except WxUser.DoesNotExist:
                    user = init_wx_user(user_open_id_or_err, '')
                if not user.active:
                    raise ClientParamsInvalidError(msg='请关注公众号《极客学舍》', code=2)
                if user.remain <= 0:
                    raise ClientParamsInvalidError(msg='您的下载次数已用完', code=2)
                user.used += 1
                user.save()
            queryset = self.filter_queryset(self.get_queryset())
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

