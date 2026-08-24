# # -*- coding: utf-8 -*-

# from __future__ import unicode_literals

# from decimal import Decimal
# import random
# import string
# import paypalrestsdk

# from django.conf import settings
# from .models import PaymentsSettings, CreditHistory
# from .exceptions import PaymentException
# from .constants import CREDIT_IN, CREDIT_OUT, OBJECT_TYPE_CONTENT
# from ..classes.constants import REQUEST_STATUS_REFUNDED, REQUEST_STATUS_CONFIRMED


# def configure_paypal():
#     paypalrestsdk.configure({
#         'mode': settings.PAYPAL_MODE,
#         'client_id': settings.PAYPAL_CLIENT_ID,
#         'client_secret': settings.PAYPAL_CLIENT_SECRET
#     })


# configure_paypal()


# def configure_openid_paypal():
#     redirect_uri = 'https://{domain}/app/profile/general'.format(
#         domain=settings.DOMAIN_NAME)
#     paypalrestsdk.configure({
#         'mode': settings.PAYPAL_MODE,
#         'client_id': settings.PAYPAL_CLIENT_ID,
#         'client_secret': settings.PAYPAL_CLIENT_SECRET,
#         'openid_redirect_uri': redirect_uri
#     })


# def student_processing_fee(teacher_rate):
#     payment_settings = PaymentsSettings.get_solo()

#     if teacher_rate < payment_settings.processing_fee_threshold:
#         processing_fee = payment_settings.processing_fee_under_threshold
#     else:
#         processing_fee = teacher_rate * \
#                          payment_settings.processing_fee_percentage_over_threshold

#     return processing_fee


# def student_total_charge(teacher_rate):
#     total_charge = teacher_rate + student_processing_fee(teacher_rate)
#     return total_charge.quantize(Decimal('0.01'))


# def create_full_paypal_refund(class_request, bundled_class_requests):
#     # Here we check if refund is  made for class whose payemnt is made using
#     # paypal or only using credits.
#     if class_request.paypal_payment_id.startswith('PAY'):
#         payment = find_paypal_payment(class_request.paypal_payment_id)
#         sale = paypalrestsdk.Sale.find(
#             payment.transactions[0].related_resources[0].sale.id)

#     teacher_rate = calculate_teacher_rate(class_request)
#     processing_fees_total = student_processing_fee(
#         sum(calculate_teacher_rate(class_request) for class_request in
#             bundled_class_requests)
#     )
#     processing_fee_to_refund = processing_fees_total / bundled_class_requests.count()

#     refund_total = teacher_rate + processing_fee_to_refund
#     refund_total = refund_total.quantize(Decimal('0.01'))

#     # check if this class_request exist in credit history and if it exists,
#     # then subtract the credit amount from the refund_total and add that amount
#     # to student credits. Also make refund entry in credit history only if
#     # credit amount is not equal to 0.
#     credit_class_request = CreditHistory.objects.filter(
#         paypal_payment_id=class_request.paypal_payment_id
#     ).order_by('updated_on')

#     if credit_class_request.count() > 0:
#         credit_class_request = credit_class_request[0]
#         student = class_request.student
#         credit_amount, paypal_amount = 0, 0

#         if credit_class_request.paypal_amount > 0:

#             if credit_class_request.paypal_amount >= refund_total:
#                 credit_class_request.paypal_amount -= refund_total
#                 paypal_amount = refund_total
#             else:
#                 credit_amount = refund_total - \
#                     credit_class_request.paypal_amount
#                 refund_total = credit_class_request.paypal_amount
#                 credit_class_request.paypal_amount = 0
#                 credit_class_request.credit_amount -= credit_amount
#                 student.credits += credit_amount
#                 paypal_amount = refund_total
#         else:
#             credit_class_request.credit_amount -= refund_total
#             credit_amount = refund_total
#             student.credits += refund_total

#         student.save()
#         credit_class_request.save()

#         CreditHistory.objects.create(
#             paypal_payment_id=class_request.paypal_payment_id,
#             student=class_request.student,
#             credit_amount=credit_amount,
#             paypal_amount=paypal_amount,
#             status=REQUEST_STATUS_REFUNDED,
#             credit_type=CREDIT_IN
#         )

#     # If tha payment was made only using credits then we will return dict
#     # instead of paypal refund object.

#     if class_request.paypal_payment_id.startswith('CRE'):
#         return {"type": "credits"}

#     refund = sale.refund({
#         'amount': {
#             'currency': 'USD',
#             'total': str(refund_total)
#         }
#     })

#     return refund


# def build_payment_string(payment_total, payment_description, redirect_url,
#                          cancel_url=None):
#     """Create paypal payment string"""
#     return paypalrestsdk.Payment({
#         'intent': 'sale',
#         'payer': {
#             'payment_method': 'paypal',
#         },
#         'transactions': [
#             {
#                 'amount': {
#                     'total': str(payment_total),
#                     'currency': 'USD',
#                 },
#                 'description': payment_description
#             }
#         ],
#         'redirect_urls': {
#             'return_url': redirect_url,
#             'cancel_url': cancel_url or redirect_url
#         }
#     })


# def create_paypal_payment(class_requests, pay_by_credit=False):

#     # PayPal appends more info in GET params
#     redirect_url = 'https://{domain}/app/dashboard/requests'.format(
#         domain=settings.DOMAIN_NAME)

#     # sum app money and join text fields if generating payment for more than
#     # one class request
#     payment_total = student_total_charge(
#         sum(
#             calculate_teacher_rate(class_request) for class_request in
#             class_requests
#         )
#     )
#     # If student has paid using credits, then if credits are more than
#     # class request's rate we update credits and return response
#     # else we deduct credits from paymet_total and redirect user to paypal
#     # to pay remaining amount
#     if pay_by_credit:
#         student = class_requests[0].student

#         if payment_total > student.credits:
#             payment_total -= student.credits
#         elif payment_total <= student.credits:
#             student.credits -= payment_total
#             credit_id = "CRE-{}".format(
#                 ''.join(
#                     random.choice(
#                         string.ascii_uppercase + string.digits
#                     ) for _ in xrange(24)
#                 )
#             )

#             for class_request in class_requests:
#                 class_request.paypal_payment_id = credit_id
#                 class_request.save()
#             CreditHistory.objects.create(
#                 paypal_payment_id=credit_id,
#                 student=student,
#                 credit_amount=payment_total,
#                 status=REQUEST_STATUS_CONFIRMED,
#                 credit_type=CREDIT_OUT
#             )
#             student.save()
#             return {'type': 'credit', 'count': len(class_requests)}

#     payment_description = ', '.join(
#         class_request.transaction_description for class_request in class_requests
#     )

#     payment = build_payment_string(
#         payment_total,
#         payment_description,
#         redirect_url
#     )

#     if payment.create():
#         for class_request in class_requests:
#             class_request.paypal_payment_id = payment.id
#             class_request.save()
#         return payment
#     else:
#         raise PaymentException(payment.error)


# def create_paypal_payment_for_content(content_download, pay_by_credit=False):
#     """Create payment for content"""
#     # PayPal appends more info in GET params
#     redirect_url = 'https://{domain}/app/dashboard/my_content'.format(
#         domain=settings.DOMAIN_NAME)
#     payment_total = content_download.content.content_price
#     # Here we decide if user is paying using credits then he will be redirected
#     # to paypal only if, he is partially paying using credit and remaining from
#     # paypal and we make entry in teh credit history table else he will be
#     # redirected to paypal to pay amount

#     if pay_by_credit:
#         student = content_download.student

#         if payment_total > student.credits:
#             payment_total -= student.credits
#         elif payment_total <= student.credits:
#             student.credits -= payment_total
#             credit_id = "CRE-{}".format(
#                 ''.join(
#                     random.choice(
#                         string.ascii_uppercase + string.digits
#                     ) for _ in xrange(24)
#                 )
#             )
#             content_download.paypal_payment_id = credit_id
#             content_download.save()
#             CreditHistory.objects.create(
#                 paypal_payment_id=credit_id,
#                 student=student,
#                 object_type=OBJECT_TYPE_CONTENT,
#                 credit_amount=payment_total,
#                 status=REQUEST_STATUS_CONFIRMED,
#                 credit_type=CREDIT_OUT
#             )
#             student.save()
#             return {'href': redirect_url}

#     payment_description = '{0}{1}'.format(
#         'Payment for buying ',
#         content_download.content.title
#     )
#     payment = build_payment_string(
#         payment_total,
#         payment_description,
#         redirect_url
#     )

#     if payment.create():
#         content_download.paypal_payment_id = payment.id
#         content_download.save()
#         return payment
#     else:
#         raise PaymentException(payment.error)


# def create_paypal_payment_for_gig(business_gig):
#     """Create paypal payment for a business gig."""
#     # PayPal appends more info in GET params
#     redirect_url = 'https://{domain}/app/dashboard/requests'.format(
#         domain=settings.DOMAIN_NAME)
#     cancel_url = 'https://{domain}/app/dashboard/requests?ref={ref}'.format(
#         domain=settings.DOMAIN_NAME,
#         ref=business_gig.pk
#     )
#     # fetch payment type field name and string
#     payment_type, payment_type_string = business_gig.payment_type.popitem()
#     payment_description = """{payment_type_string} for {subject} class
#     requested on {created_on}""".format(
#         subject=business_gig.subject,
#         payment_type_string=payment_type_string,
#         created_on=business_gig.created_on.strftime('%c')
#     )
#     # listed here to be explicit and clear in the build_payment_string method
#     payment_total = getattr(business_gig, payment_type)
#     payment = build_payment_string(
#         payment_total,
#         payment_description,
#         redirect_url,
#         cancel_url
#     )

#     if payment.create():
#         business_gig.payments[payment_type] = payment.id
#         business_gig.save()
#         return payment
#     else:
#         raise PaymentException(payment.error)


# def find_paypal_payment(payment_id):
#     return paypalrestsdk.Payment.find(payment_id)


# def execute_paypal_payment(payment):
#     return payment.execute({'payer_id': payment.payer.payer_info.payer_id})


# def create_paypal_payout(class_requests):

#     if not all(class_request.teacher == class_requests[0].teacher
#                for class_request in class_requests):

#         raise PaymentException(
#             'Cannot create paypal payout for class requests belonging to '
#             'different teachers. Call create_paypal_payout separately for '
#             'class requests of every teacher.')

#     payment_settings = PaymentsSettings.objects.get()
#     payout_recipient = class_requests[0].teacher.paypal_account
#     # sum class requests for student and businesses separately
#     payout_sum = 0
#     business_payout_sum = 0

#     for class_request in class_requests:
#         if class_request.student is not None:
#             payout_sum += class_request.teacher_payout
#         elif class_request.business is not None:
#             # do not deduct 15% or trnasaction fee percentage for business
#             # requests
#             business_payout_sum += class_request.teacher_payout_for_business

#     # we deduct PayPal fees from teachers payouts
#     payout_fee = min(
#         payout_sum * payment_settings.paypal_payout_fee_percentage,
#         payment_settings.paypal_payout_fee_cap
#     )
#     payout_sum -= payout_fee
#     # do not deduct paypal fees from teacher payout for business requests
#     payout_sum += business_payout_sum
#     payout_sum = payout_sum.quantize(Decimal('0.01'))
#     description = 'Payment for LearnSkillz classes'
#     payout = paypalrestsdk.Payout({
#         'sender_batch_header': {
#             'email_subject': 'LearnSkillz payment'
#         },
#         'items': [
#             {
#                 'recipient_type': 'EMAIL',
#                 'amount': {
#                     'value': str(payout_sum),
#                     'currency': 'USD',
#                 },
#                 'receiver': payout_recipient,
#                 'note': description
#             }
#         ]
#     })

#     if payout.create(sync_mode=True):
#         return payout
#     else:
#         raise PaymentException(payout.error)


# def create_paypal_payout_for_content(content_downloads):
#     """Create paypal payout for all content that the teacher sold"""
#     if not all(content_download.content.teacher ==
#                content_downloads[0].content.teacher
#                for content_download in content_downloads):

#         raise PaymentException(
#             'Cannot create paypal payout for content belonging to '
#             'different teachers. Call create_paypal_payout_for_content'
#             'separately for content download of every teacher.')

#     payout_recipient = content_downloads[0].content.teacher.paypal_account
#     payout_sum = sum(
#         content_download.content.teacher_payout for content_download
#         in content_downloads
#     )
#     payout_sum = payout_sum.quantize(Decimal('0.01'))

#     description = 'Payment for LearnSkillz Content'
#     payout = paypalrestsdk.Payout({
#         'sender_batch_header': {
#             'email_subject': 'LearnSkillz payment for Content Downloads'
#         },
#         'items': [
#             {
#                 'recipient_type': 'EMAIL',
#                 'amount': {
#                     'value': str(payout_sum),
#                     'currency': 'USD',
#                 },
#                 'receiver': payout_recipient,
#                 'note': description
#             }
#         ]
#     })

#     if payout.create(sync_mode=True):
#         return payout
#     else:
#         raise PaymentException(payout.error)


# def calculate_teacher_rate(class_request):
#     """
#     This method was added when the coupon codes functionality was implemented.
#     The method accepts a class request and checks if it contains a coupon code,
#     which might have been applied at the time of requesting the class.
#     If it has a coupon code, then the discounted class rate is returned
#     otherwise the teacher_rate is returned without a change
#     The teacher payout is calculated in the classes model in the teacher payout
#     property
#     """
#     if class_request.coupon_code:
#         return class_request.teacher_rate * (1 - (class_request.coupon_code.discount/100))
#     else:
#         return class_request.teacher_rate


# def generate_paypal_agreement(membership_plan_id, start_date):
#     """
#     Function handles the task of creating billing agreement
#     for recurring payments
#     """
#     payment_settings = PaymentsSettings.objects.get()
#     agreement_info = {
#         'description': payment_settings.agreement_description,
#         'name': 'Learnskillz Premium Membership',
#         'plan_id': membership_plan_id,
#         'start_date': start_date
#     }

#     billing_agreement = paypalrestsdk.BillingAgreement({
#         "name": agreement_info['name'],
#         "description": agreement_info['description'],
#         "start_date": agreement_info['start_date'],
#         "plan": {
#             "id": membership_plan_id
#         },
#         "payer": {
#             "payment_method": "paypal",
#         },

#     })

#     return billing_agreement


# def agreement_execute(token):
#     return paypalrestsdk.BillingAgreement.execute(token)


# def cancel_agreement(agreement_id):
#     try:
#         billing_agreement = paypalrestsdk.BillingAgreement.find(agreement_id)
#         print("Billing Agreement [%s] has state %s" %
#               (billing_agreement.id, billing_agreement.state))

#         cancel_note = {
#             "note": "Cancelling the agreement"
#         }

#         if billing_agreement.cancel(cancel_note):
#             return True
#         else:
#             return False

#     except paypalrestsdk.ResourceNotFound as error:
#         return False


# def verify_webhook(request):
#     """
#     Call the rest sdk WebhookEvent and verify that the POST data is genuinely
#     coming from PayPal.

#     When in doubt https://github.com/paypal/PayPal-Python-SDK/issues/196
#     """
#     payment_settings = PaymentsSettings.objects.get()
#     return paypalrestsdk.WebhookEvent.verify(
#         transmission_id=request.META['HTTP_PAYPAL_TRANSMISSION_ID'],
#         timestamp=request.META['HTTP_PAYPAL_TRANSMISSION_TIME'],
#         webhook_id=payment_settings.webhook_id,
#         event_body=request.body,
#         cert_url=request.META['HTTP_PAYPAL_CERT_URL'],
#         actual_sig=request.META['HTTP_PAYPAL_TRANSMISSION_SIG'],
#         auth_algo=request.META['HTTP_PAYPAL_AUTH_ALGO']
#     )


# def get_validate_url():
#     configure_openid_paypal()
#     return paypalrestsdk.Tokeninfo.authorize_url({'scope': 'openid email'})


# def create_token_with_code(code):
#     return paypalrestsdk.Tokeninfo.create(code)
