"""
All exception classes
"""

from traceback import format_exc, print_exc

from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.response import Response
from rest_framework.views import exception_handler


def handler404(request):
    return render(request, '404.html', status=404)


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Raised Conflict while processing request"
    default_code = 'conflict'


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Exception raised because of invalid data.'
    default_code = 'bad_request'


class InvalidData(APIException):
    """
    raise InvalidData({"field":"error"}, message="my msg") -> {
        "message": "my msg",
        "error": {"field":"error"}
    }

    raise InvalidData({"field":"error"}) -> {
        "message": "error",
        "error": {"field":"error"}
    }

    raise InvalidData({"field1":"error1", "field2":"error2" }) -> {
        "message": "Invalid Data",
        "error": { "field1": "error1", "field2": "error2" }
    }

    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, message=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if message is not None:
            self.message = message

        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

