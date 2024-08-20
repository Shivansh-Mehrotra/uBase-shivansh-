import base64
from datetime import datetime
from django.conf import settings
from django.core.signing import loads, dumps, BadSignature, SignatureExpired
from rest_framework import serializers


def base64decode(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.urlsafe_b64decode(base64_bytes)
    return message_bytes.decode('ascii')


def base64encode(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.urlsafe_b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def make_token(data):
    return base64encode(dumps(data))


def check_token(token, valid_for_seconds=None, raise_exception=False):
    try:
        return loads(base64decode(token), max_age=valid_for_seconds)
    except Exception as e:
        if raise_exception:
            raise
    return False


def get_token_data(token):
    return loads(base64decode(token))


# DRF serializers.Field
class TokenSerializerField(serializers.Field):
    default_error_messages = {
        'expired': 'Token has expired.',
        'invalid': 'Invalid token.',
    }

    def __init__(self, **kwargs):
        self.return_data = kwargs.pop('return_data', False)
        super().__init__(**kwargs)

    def to_representation(self, value):
        if self.return_data:
            return self.token_data
        return value

    def to_internal_value(self, data):
        try:
            self.token_data = check_token(data, settings.DEFAULT_USER_EVENT_LIFETIME, raise_exception=True)
        except SignatureExpired as e:
            self.fail('expired')
        except Exception as e:
            self.fail('invalid')
        return data



