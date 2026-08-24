# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from .constants import (
    CREDIT_TYPE_CHOICES, OBJECT_TYPE_CHOICE,
    OBJECT_TYPE_CLASS, REQUEST_STATUS_CHOICES
)


# Create your models here.
class PaymentsHistory(models.Model):
    class Meta:
        verbose_name = 'Subscription Payments History'
        verbose_name_plural = 'Subscription Payments History'

    user = models.ForeignKey(
        'profiles.Profile',
        related_name='subscription_history'
    )
    # paypal_payment_id = models.CharField(
    #     max_length=50,
    #     blank=True,
    #     null=True
    # )
    agreement_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    event_type = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    subscription_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Subscription price')
    )
    payment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Paid by: {} Amount: {} on {} >'.format(
            self.user,
            self.subscription_price,
            self.payment_date
        )


class CreditHistory(models.Model):
    paypal_payment_id = models.CharField(max_length=50, blank=True, null=True)
    student = models.ForeignKey(
        'accounts.Student',
        verbose_name=_('Student'),
        related_name='student_credit_history',
        null=True,
        blank=True
    )
    credit_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Credit Amount'),
        default=0
    )
    paypal_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Paypal Amount'),
        default=0
    )
    status = models.IntegerField(
        choices=REQUEST_STATUS_CHOICES,
        verbose_name=_('Request status')
    )
    object_type = models.IntegerField(
        choices=OBJECT_TYPE_CHOICE,
        default=OBJECT_TYPE_CLASS
    )
    credit_type = models.IntegerField(
        choices=CREDIT_TYPE_CHOICES
    )
    updated_on = models.DateTimeField(
        auto_now_add=True,
        help_text=_('This is the time, when credit was added or it was used')
    )
