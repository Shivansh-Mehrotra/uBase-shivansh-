"""
The Response class in REST framework is similar to HTTPResponse, except that
it is initialized with unrendered data, instead of a pre-rendered string.

The appropriate renderer is called during Django's template response rendering.
"""
from http.client import responses

from django.conf import settings
from django.template.response import SimpleTemplateResponse
from rest_framework import status
from rest_framework.response import Response

from rest_framework.serializers import Serializer


class SimpleMessageResponse(Response):
    """
    An HttpResponse that allows to send simple success message
    """

    def __init__(self, message=None, http_status=status.HTTP_200_OK):
        """
        Alters the init arguments slightly.
        """

        if not isinstance(message, str):
            msg = (
                'You passed a %s instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. represemntation.'
            )
            raise AssertionError(msg % type(message))

        super().__init__({
            settings.DEFAULT_MESSAGE_KEY: message
        }, status=http_status)


class SimpleDataResponse(Response):
    """
    An HttpResponse that allows to send simple success data message
    """

    def __init__(self, data=None, http_status=status.HTTP_200_OK):
        """
        Alters the init arguments slightly.
        """
        if data is None:
            data = {}

        super().__init__({
            settings.DEFAULT_MESSAGE_KEY: settings.DEFAULT_SUCCESS_MESSAGE,
            "data": data
        }, status=http_status)