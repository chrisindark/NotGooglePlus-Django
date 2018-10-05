# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import JsonResponse

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from .models import PaymentsSettings, PaymentsHistory
from ..notifications.notifications import (
    send_membership_renewed_email,
    send_membership_payment_pending,
    send_membership_activation_email,
    send_membership_cancel_email
)
from ..payments.paypal import (
    generate_paypal_agreement,
    agreement_execute,
    cancel_agreement,
    verify_webhook
)


class PaymentResourcesView(APIView):

    def get(self, request, *args, **kwargs):
        serialized_data = {
            'membership_subscription_fee':
                PaymentsSettings.get_solo().membership_subscription_fee,
        }
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK
        )


class PaymentMemberShipView(APIView):
    permissions_classes = (IsTeacher,)

    def get(self, request, *args, **kwargs):
        """
        start_date set to one month later for teacher already having trial
        and get plan_id of plan having setup_fee and no trial,
        else set start_date to today's date get plan_id having trial of one
        month
        """
        teacher = Teacher.objects.get(pk=self.request.user.teacher.id)
        ps = PaymentsSettings.objects.get()

        if teacher.had_trial or teacher.is_on_trial:
            start_date = (
                datetime.utcnow() + relativedelta(months=1)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
            billing_agreement = generate_paypal_agreement(
                ps.membership_plan_without_trial_id,
                start_date
            )
        else:
            start_date = (
                datetime.utcnow() + timedelta(hours=1)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
            billing_agreement = generate_paypal_agreement(
                ps.membership_plan_with_trial_id,
                start_date
            )
        if not teacher.paypal_agreement_id:
            if billing_agreement.create():
                payment_approval_url = next(
                    link for link in billing_agreement.links if link.rel == 'approval_url'
                )
                return JsonResponse(
                    {'payment_link': payment_approval_url.href}
                )
            else:
                response = JsonResponse(
                    {'non_field_errors':
                        'Error Occured. Please Try Again Later '})
                response.status_code = 400
        else:
            response = JsonResponse({'non_field_errors':
                                    'You Have Already Subscribed'})

        response.status_code = 400
        return response


class PaymentMemberShipConfirmView(APIView):
    permissions_classes = (IsTeacher,)

    def get(self, request, *args, **kwargs):
        token = self.request.GET['token']
        teacher = Teacher.objects.get(pk=self.request.user.teacher.id)
        if not teacher.paypal_agreement_id:
            agreement = agreement_execute(token)
            if not agreement.error:
                count = Teacher.objects.filter(
                    paypal_agreement_id=agreement['id']
                ).count()
                if count == 0:
                    teacher.paypal_agreement_id = agreement['id']
                    teacher.membership_status = TEACHER_MEMBERSHIP_PREMIUM
                    if teacher.never_had_trial:
                        teacher.trial_status = TEACHER_MEMBERSHIP_IS_ON_TRIAL
                    elif teacher.is_on_trial:
                        teacher.trial_status =\
                            TEACHER_MEMBERSHIP_TRIAL_COMPLETED
                    teacher.save()
                    send_membership_activation_email(teacher)
                    return JsonResponse({'status': 'Successfully Subscribed'})
                else:
                    response = JsonResponse(
                        {'non_field_errors':
                            'Error Occured. Please Contact Learnskillz'})
                    response.status_code = 400
            else:
                    response = JsonResponse(
                        {'non_field_errors':
                            'Error Occured. Please Contact Learnskillz'})
                    response.status_code = 400

        else:
            response = JsonResponse(
                {'non_field_errors':
                    'You Have Already Subscribed'})

        response.status_code = 400
        return response


class PaymentMemberShipCancelView(APIView):
    """
    Teacher will still remain premium after cancelling its membership
    """
    permissions_classes = (IsTeacher,)

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(pk=self.request.user.teacher.id)
        agreement_id = teacher.paypal_agreement_id
        result = cancel_agreement(agreement_id)

        if teacher.is_on_trial:
            teacher.trial_status = TEACHER_MEMBERSHIP_TRIAL_COMPLETED
            teacher.save()

        if result:
            teacher.membership_status = TEACHER_MEMBERSHIP_CANCELED
            teacher.save()
            teacher.cancel_membership()
            return JsonResponse({'status': 'Successfully UnSubscribed'})
        else:
            response = JsonResponse({'non_field_errors':
                                     'Error Occured'})
            response.status_code = 400
            return response


class WebhookView(APIView):
    http_method_names = ['post']

    def _payment_not_present(self, resource):
        """
        Webhook validation.

        Webhooks are asynchronous, their order is not guaranteed,
        and idempotency might lead to a duplicate notification of the
        same event type.
        """
        try:
            PaymentsHistory.objects.get(
                paypal_payment_id=resource['id'],
            )
            return False
        except PaymentsHistory.DoesNotExist:
            return True
        except PaymentsHistory.MultipleObjectsReturned:
            return False

    def post(self, request, *args, **kwargs):
        if (verify_webhook(request) and
                self._payment_not_present(request.data['resource'])):
            data = request.data

            if data['event_type'] == 'PAYMENT.SALE.COMPLETED':
                resource = data['resource']

                if 'billing_agreement_id' in resource:
                    teacher = Teacher.objects.get(
                        paypal_agreement_id=resource['billing_agreement_id']
                    )
                    all_data = {
                        'teacher': teacher,
                        'paypal_payment_id': resource['id'],
                        'agreement_id': resource['billing_agreement_id'],
                        'payment_date': resource['create_time'],
                        'event_type': data['event_type'],
                        'subscription_price': resource['amount']['total']
                    }

                    if teacher.is_on_trial:
                        teacher.status = TEACHER_MEMBERSHIP_TRIAL_COMPLETED
                        teacher.save()
                    PaymentsHistory.objects.create(**all_data)

                    from_date = str(parse(resource['create_time']).date())
                    to_date = str(
                        (
                            parse(resource['create_time']) +
                            relativedelta(months=1)
                        ).date()
                    )
                    send_membership_renewed_email(
                        teacher,
                        resource['amount']['total'],
                        from_date,
                        to_date
                    )

            elif data['event_type'] == 'BILLING.SUBSCRIPTION.CANCELLED':
                teacher = Teacher.objects.get(
                    paypal_agreement_id=data['resource']['id']
                )
                teacher.cancel_membership()
                all_data = {
                    'teacher': teacher,
                    'agreement_id': data['resource']['id'],
                    'payment_date': data['create_time'],
                    'event_type': data['event_type'],
                }
                PaymentsHistory.objects.create(**all_data)
                send_membership_cancel_email(teacher)

            elif data['event_type'] == 'PAYMENT.SALE.PENDING':
                resource = data['resource']
                if 'billing_agreement_id' in resource:
                    teacher = Teacher.objects.get(
                        paypal_agreement_id=resource['billing_agreement_id']
                    )
                    send_membership_payment_pending(teacher)

            elif data['event_type'] == 'BILLING.SUBSCRIPTION.CREATED':
                teacher = Teacher.objects.get(
                    paypal_agreement_id=data['resource']['id']
                )
                all_data = {
                    'teacher': teacher,
                    'agreement_id': data['resource']['id'],
                    'payment_date': data['create_time'],
                    'event_type': data['event_type'],
                }
                PaymentsHistory.objects.create(**all_data)

        return Response(status=status.HTTP_200_OK)
