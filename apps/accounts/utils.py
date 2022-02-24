import os
import binascii

from datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template import loader


class UserEmailManager(object):
    user = None

    @staticmethod
    def generate_activation_key():
        security_key = binascii.hexlify(os.urandom(20)).decode()
        security_key_expires = datetime.now() + timedelta(days=7)
        return security_key, security_key_expires

    @staticmethod
    def send_email(subject_template_name, email_template_name,
                   context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_response = email_message.send()
        return email_response
