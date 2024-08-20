from django.utils.crypto import get_random_string

default_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def get_salt_string(length=12, chars=None):
    '''
    to generate salt like secret_key

    Reference:
    .../site-packages/django/core/management/commands/startproject.py

    :param length:
    :param chars:
    :return:
    '''
    return get_random_string(length, chars or default_chars)
