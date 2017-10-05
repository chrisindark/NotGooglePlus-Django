# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.template.context import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode


def mail(
        recipient_list,
        template_name,
        from_email=settings.DEFAULT_FROM_EMAIL,
        context=None):
    """Default email function."""
    context = {} if context is None else context
    template_filename = settings.EMAIL_TEMPLATE_FILE_FORMAT.format(
        template_name=template_name
    )
    template = get_template(template_filename)
    subject, content, plain_content = '', '', ''
    context = Context(context)
    context.template = getattr(template, 'template', template)

    for node in template.template:
        if isinstance(node, BlockNode) and node.name == 'subject':
            subject = node.render(context)
        if isinstance(node, BlockNode) and node.name == 'content':
            content = node.render(context)
        if isinstance(node, BlockNode) and node.name == 'plain_content':
            plain_content = node.render(context)

    return send_mail(
        subject=subject,
        message=plain_content,
        html_message=content,
        from_email=from_email,
        recipient_list=recipient_list
    )
