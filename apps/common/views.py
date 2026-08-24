from zoneinfo import available_timezones

import django_countries
from rest_framework import status, views
from rest_framework.response import Response


# # Create your views here.
class ResourcesView(views.APIView):
    """
    Serve choices
    """

    @staticmethod
    def get_resources_list(choices):
        return [{"id": id_number, "name": name} for id_number, name in choices]

    def get(self, request, *args, **kwargs):
        timezones = sorted(available_timezones())

        countries = self.get_resources_list(list(django_countries.countries))
        serialized_data = {"timezones": timezones, "countries": countries}

        return Response(data=serialized_data, status=status.HTTP_200_OK)
