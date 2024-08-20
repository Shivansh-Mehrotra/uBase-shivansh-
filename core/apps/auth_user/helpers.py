import uuid
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import base64
import urllib
import json

from django.core.signing import TimestampSigner

from core.apps.notification.notification_helper import send_email_notification
from core.tokens import make_token

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


# def send_welcome_mail(user, path=None, email=None):
#     url_encoded_data = base64encode(user)
#     url = path + "/auth/reset-password/?token=" + url_encoded_data
#     subject = SUBJECTS[WELCOMEMAIL]
#     template_context = {
#         'user': user.first_name + user.last_name,
#         'password_reset_link': url
#     }
#     context = {
#         'to': [email if email else user.email],
#         'subject': subject,
#         'template': WELCOMEMAIL,
#         'template_context': template_context
#     }
#     is_sent, response = send_email_notification(context)
#     return is_sent


def send_reset_password_mailer(user, path=None):

    token_payload = {
        "user_id": user.id,
        "email": user.email,
        'iat': datetime.now().timestamp() * 1000
    }

    password_reset_url = path if path else settings.PASSWORD_RESET_URL

    to = [user.email]
    token = make_token(token_payload)
    template_context = {
        "branding_logo": settings.BRANDING_LOGO,
        'token': token,
        'user': user.first_name + user.last_name,
        'password_reset_url': f'{password_reset_url}?token={token}'
    }
    context = {
        'subject': "Reset password mail",
        'template': 'reset_password.html',
        'template_context': template_context
    }

    is_sent, response = send_email_notification(to, **context)
    print(response)
    return is_sent


# def send_reset_email(user, path=None, email=None):
#     url_encoded_data = base64encode(user)
#     url = path + "/auth/reset-password/?token=" + url_encoded_data
#
#     subject = 'Reset Password Link'
#
#     # plain_message = 'Username - {} has a password reset link is <br> {}'.format(user.email,url)
#     plain_message = 'Below is your password reset link for {} <br> {}'.format(user.email,url)
#     if not email:
#         email = user.email
#     to = email
#     try:
#         sent = send_mail(subject, plain_message,EMAIL_HOST_USER,[to])
#     except Exception as e:
#         print(e)
#         return False
#     return True
