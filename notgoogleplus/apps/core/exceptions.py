from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.views import exception_handler


class ServiceUnavailable(APIException):
    status_code = HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('Service temporarily unavailable, try again later.')
    default_code = 'service_unavailable'


def custom_exception_handler(exc, context):
    # If an exception is thrown that we don't explicitly handle here, we want
    # to delegate to the default exception handler offered by DRF. If we do
    # handle this exception type, we will still want access to the response
    # generated by DRF, so we get that response up front.

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    handlers = {
        'NotFound': _handle_not_found_error,
        'ValidationError': _handle_generic_error
    }
    # This is how we identify the type of the current exception. We will use
    # this in a moment to see whether we should handle this exception or let
    # Django REST Framework do it's thing.
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # If this exception is one that we can handle, handle it. Otherwise,
        # return the response generated earlier by the default exception
        # handler.
        return handlers[exception_class](exc, context, response)

    return response


def _handle_not_found_error(exc, context, response):
    return response


def _handle_generic_error(exc, context, response):
    # This is about the most straightforward exception handler we can create.

    # We can add the HTTP status code to the response.
    # response.data['status_code'] = response.status_code

    # The array of validation errors is convert to string
    if response is not None:
        for key, value in response.data.items():
            if isinstance(value, list):
                response.data[key] = value[0]

    return response
