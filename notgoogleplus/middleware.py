import logging

from django.db import connection
from django_redis import get_redis_connection

from apps.core.models import AppModel

logger = logging.getLogger(__name__)


class QueryCountDebugMiddleware(object):
    """
    This middleware will log the number of queries run
    and the total time taken for each request (with a
    status code of 200). It does not currently support
    multi-db setups.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) is called.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if response.status_code == 200:
            total_time = 0

            for query in connection.queries:
                # logger.debug('%s query ==== ' % query)
                query_time = query.get('time')
                if query_time is None:
                    # django-debug-toolbar monkeypatches the connection
                    # cursor wrapper and adds extra information in each
                    # item in connection.queries. The query time is stored
                    # under the key "duration" rather than "time" and is
                    # in milliseconds, not seconds.
                    query_time = query.get('duration', 0) / 1000
                total_time += float(query_time)

            logger.debug('%s queries run, total %s seconds' %
                         (len(connection.queries), total_time))
            # print('%s queries run, total %s seconds' % (len(connection.queries), total_time))
        return response


class AppVersionMiddleware(object):
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
        redis_connection = get_redis_connection('default')
        try:
            app_version = redis_connection.get('core:app_version')
        except Exception as e:
            app_version = None
            logger.error(e)

        if app_version:
            response['Notgoogleplus-App-Version'] = app_version
            return response

        # get the app_version from db
        app_model = AppModel.objects.first()
        app_version = app_model.app_version
        redis_connection.set('core:app_version', app_version)
        if app_model:
            response['Notgoogleplus-App-Version'] = app_version
            request.session['notgoogleplus_app_version'] = app_version
        # if request.session has app version, set it as it is, but dont understand why should we
        elif request.session.get('notgoogleplus_app_version', False):
            response['Notgoogleplus-App-Version'] = request.session.get(
                'notgoogleplus_app_version')
        else:
            logger.error("AppModel isnt initiated.")

        return response
