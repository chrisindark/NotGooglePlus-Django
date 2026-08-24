import logging
import time
import uuid

from apps.core.models import AppConfig
from core.constants import CORRELATION_ID_HEADER, NOTGOOGLEPLUS_APP_VERSION_HEADER
from core.request_context import correlation_id

logger = logging.getLogger(__name__)


class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        c_id = request.headers.get(CORRELATION_ID_HEADER, str(uuid.uuid4()))

        correlation_id.set(c_id)
        request.correlation_id = c_id

        response = self.get_response(request)
        response[CORRELATION_ID_HEADER] = c_id

        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration": round(duration, 3),
                "user_id": getattr(request.user, "id", None),
            },
        )

        return response


class AppVersionMiddleware:
    """
    This middleware will add application version to the
    headers of every response object.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) is called.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # get the app_version from redis
        # redis_connection = get_redis_connection("default")
        # try:
        #     app_version = redis_connection.get("core:app_version")
        # except Exception as e:
        #     app_version = None
        #     logger.error(e)

        # if app_version:
        #     response["Notgoogleplus-App-Version"] = app_version
        #     return response

        # get the app_version from db
        app_model = AppConfig.get_solo()
        app_version = app_model.app_version
        # redis_connection.set("core:app_version", app_version)
        if app_model:
            response[NOTGOOGLEPLUS_APP_VERSION_HEADER] = app_version
            request.session[NOTGOOGLEPLUS_APP_VERSION_HEADER] = app_version
        else:
            logger.error("AppConfig isnt initiated.")

        return response
