"""
All exception classes
"""

from traceback import format_exc, print_exc

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.response import Response
from rest_framework.views import exception_handler

DEFAULT_MESSAGE_KEY = 'message'
if hasattr(settings, 'DEFAULT_MESSAGE_KEY'):
    DEFAULT_MESSAGE_KEY = settings.DEFAULT_MESSAGE_KEY

DEFAULT_ERROR_MESSAGE = 'Error Processing Request'
if hasattr(settings, 'DEFAULT_ERROR_MESSAGE'):
    DEFAULT_ERROR_MESSAGE = settings.DEFAULT_ERROR_MESSAGE

SHOW_ERROR_IN_MESSAGE = False
if hasattr(settings, 'SHOW_ERROR_IN_MESSAGE'):
    SHOW_ERROR_IN_MESSAGE = settings.SHOW_ERROR_IN_MESSAGE


def parse_nested_error(e):
    m = ''
    _ = {}
    if isinstance(e, str):
        return e, e
    if isinstance(e, dict):
        for k, e_l in e.items():
            m, __ = parse_nested_error(e_l)
            _[k] = m
    if isinstance(e, list):
        for e_d in e:
            m, __ = parse_nested_error(e_d)
            if m and __:
                return m, __
    return m, _


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        error = response.data
        message = DEFAULT_ERROR_MESSAGE

        if 'detail' in error:
            # normal APIException
            message = error.get('detail', message)
            error = {}
        else:
            # serializer APIException
            _msg, error = parse_nested_error(error)

            if SHOW_ERROR_IN_MESSAGE:
                message = _msg

            if not message:
                message = DEFAULT_ERROR_MESSAGE

        if hasattr(exc, 'message'):
            message = getattr(exc, 'message')

        response.data = {
            DEFAULT_MESSAGE_KEY: message,
            'error': error,
        }

    if response is None:
        response = Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'message': str(exc),
                'error': {},
                'data': {}
            }
        )

        print_exc()

        if settings.DEBUG:
            response.data['traceback'] = format_exc()

    return response

