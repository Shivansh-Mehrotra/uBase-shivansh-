"""
Basic building blocks for generic api view class for ubase app.
Modified by: Umbrella Infocare Pvt. Ltd.
"""
from __future__ import unicode_literals

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils import model_meta

from core import exceptions

DEFAULT_MESSAGE_KEY = 'message'
if hasattr(settings, 'DEFAULT_MESSAGE_KEY'):
    DEFAULT_MESSAGE_KEY = settings.DEFAULT_MESSAGE_KEY


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def creating_process(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        serializer = self.creating_process(request, *args, **kwargs)
        # TODO: check for return type of creating_process -> serializer
        headers = self.get_success_headers(serializer.data)
        message = self.response_message if self.response_message else 'Created'
        return Response({
            DEFAULT_MESSAGE_KEY: message,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        kwargs = self.get_serializer_save_kwargs(serializer)
        if 'created_by' in serializer.fields and self.request.user.id \
                and self.set_request_user_tracking:
            kwargs['created_by'] = self.request.user.id
        serializer.save(**kwargs)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(object):
    """
    List a queryset.
    """
    set_ordering_fields = True

    def get_ordering_filter(self):
        try:
            return list(self.ordering_fields_mapping.keys())
        except:
            pass

    def listing_process(self, request, *args, **kwargs):
        return self.filter_queryset(self.get_queryset())

    def list(self, request, *args, **kwargs):
        data = self.listing_process(request, *args, **kwargs)
        # TODO: check for return type of listing_process -> queryset
        page = self.paginate_queryset(data)
        if page is None:
            if settings.DEBUG:
                raise Exception("Pagination should not be missed. Please check "
                                "settings.REST_FRAMEWORK.DEFAULT_PAGINATION_CLASS"
                                "for default pagination class and set "
                                "'core.pagination.BasePagination'")
            page = []
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)

        if self.set_ordering_fields:
            response.data['sortable'] = self.get_ordering_filter()

        return response


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieving_process(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.get_serializer(instance)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.retrieving_process(request, *args, **kwargs)
        # TODO: check for return type of creating_process -> serializer
        message = self.response_message if self.response_message else 'Success'
        return Response({
            'data': serializer.data,
            DEFAULT_MESSAGE_KEY: message
        })


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

    def updating_process(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return serializer

    def update(self, request, *args, **kwargs):
        serializer = self.updating_process(request, *args, **kwargs)
        # TODO: check for return type of creating_process -> serializer
        instance = serializer.instance
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        message = self.response_message if self.response_message else 'Updated'
        return Response({
            'data': serializer.data,
            DEFAULT_MESSAGE_KEY: message
        })

    def perform_update(self, serializer):
        kwargs = self.get_serializer_save_kwargs(serializer)
        if 'updated_by' in serializer.fields and self.request.user.id \
                and self.set_request_user_tracking:
            kwargs['updated_by'] = self.request.user.id
        serializer.save(**kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def process_destroying(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

    def destroy(self, request, *args, **kwargs):
        self.process_destroying(request, *args, **kwargs)
        message = self.response_message if self.response_message else 'Deleted'
        return Response({
            DEFAULT_MESSAGE_KEY: message,
            'data': {}
        }, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class SoftDestroyModelMixin(object):
    """
    Soft destroy a model instance.
    """

    def process_soft_destroying(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_soft_destroy(instance)

    def soft_destroy(self, request, *args, **kwargs):
        self.process_soft_destroying(request, *args, **kwargs)
        message = self.response_message if self.response_message else 'Deleted'
        return Response({
            DEFAULT_MESSAGE_KEY: message,
            'data': {}
        }, status=status.HTTP_200_OK)

    def perform_soft_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


