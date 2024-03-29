# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import connection

# from apps.core.models import AppModel

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
        # app_model = AppModel.objects.first()
        # if app_model:
        #     response['App-Version'] = app_model.app_version
        # if request.session.get('app_version', False):
        #     response['App-Version'] = request.session.get('app_version')
        # else:
        #     request.session['app_version'] = app_model.app_version
        #     response['App-Version'] = request.session.get('app_version')

        return response
