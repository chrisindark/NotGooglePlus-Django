import django_countries

from rest_framework import views, status
from rest_framework.response import Response

from .utils import get_timezones


# Create your views here.
class ResourcesView(views.APIView):
    """
    Serve choices
    """
    @staticmethod
    def get_resources_list(choices):
        return [{'id': id_number, 'name': name} for id_number, name in choices]

    def get(self, request, *args, **kwargs):
        timezones = get_timezones()
        countries = self.get_resources_list(
            list(django_countries.countries)
        )
        serialized_data = {
            'timezones': timezones,
            'countries': countries
        }

        return Response(data=serialized_data, status=status.HTTP_200_OK)

