"""
Basic building blocks for generic api view class for ubase app.
Modified by: Umbrella Infocare Pvt. Ltd.
"""
from __future__ import unicode_literals

from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from core import viewmixins


class ModelViewSet(viewmixins.CreateModelMixin,
                   viewmixins.RetrieveModelMixin,
                   viewmixins.UpdateModelMixin,
                   viewmixins.DestroyModelMixin,
                   viewmixins.SoftDestroyModelMixin,
                   viewmixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    _response_message = settings.DEFAULT_SUCCESS_MESSAGE
    set_request_user_tracking = False

    @property
    def response_message(self):
        return self._response_message

    @response_message.setter
    def response_message(self, message):
        self._response_message = message

    _serializer_save_kwargs = {}

    def get_serializer_save_kwargs(self, serializer):
        return self._serializer_save_kwargs
