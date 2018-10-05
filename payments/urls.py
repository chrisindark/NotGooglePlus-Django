# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    PaymentResourcesView,
    PaymentMemberShipView,
    PaymentMemberShipConfirmView,
    PaymentMemberShipCancelView,
    WebhookView,
)

urlpatterns = patterns(
    '',
    url(
        r'^resources/$',
        PaymentResourcesView.as_view(),
        name='membership_resource'
    ),
    url(
        r'^payment/$',
        PaymentMemberShipView.as_view(),
        name='membership_payment'
    ),
    url(
        r'^payment_confirm/$',
        PaymentMemberShipConfirmView.as_view(),
        name='refresh_payments_status'
    ),
    url(
        r'^suspend/$',
        PaymentMemberShipCancelView.as_view(),
        name='membership_cancel'
    ),
    url(
        r'^payment/status/$',
        WebhookView.as_view(),
        name='payment_complete_denied'
    ),
)
