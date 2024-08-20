from django.core.mail import send_mail, EmailMultiAlternatives
# from config.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SUPPORT_MAIL, WEBSITE_BASE_URL
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.utils.html import strip_tags

from .template_constants import TEMPLATES
from django.template.loader import render_to_string
from collections import namedtuple


def send_email(
        subject=None, template=None, template_context=None, from_id=None, to=None,
        cc=None, bcc=None, attachments=None, reply_to=None
):
    html_content = render_to_string(template, template_context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_id, to, bcc=bcc, cc=cc, reply_to=reply_to)
    msg.attach_alternative(html_content, "text/html")
    # TODO: handle attachments with str, file like obj, auto mime type
    response = msg.send()
    return response


def send_email_notification(to, **context):
    assert to, "To is required"
    assert context, "Email Context is required"

    try:
        response = send_email(
            to=to,
            subject=context['subject'],
            template=context['template'],
            template_context=context['template_context'],
            # from_id=context['from_id'],
            cc=None,
            bcc=None,
            attachments=None,
            # reply_to=context['reply_to'],
        )
        return True, response
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, str(e)


