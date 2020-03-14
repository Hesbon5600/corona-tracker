from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
# local imports
from .serializers import (GeneralStatsSerializer, CountryStatsSerializer)
from .helpers.renderers import RequestJSONRenderer
from .helpers.pagination_helper import Pagination
from .helpers.scrap_data import fech_data
from .models import GeneralStats, CountryCases


class GeneralStatsAPIView(generics.GenericAPIView):

    renderer_classes = (RequestJSONRenderer,)
    serializer_class = GeneralStatsSerializer

    def get(self, request):
        """
        Get the general stats
        """
        print(
            f"\n\n\n\n[<<<<<<<{request.META.get('HTTP_REFERER', '') or request.headers.get('User-Agent', '')}>>>>>>>>>]\n\n\n\n")

        queryset = GeneralStats.objects.all().order_by('-created_at').first()
        serializer = self.serializer_class(
            queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListSearchCountriesAPIView(viewsets.ReadOnlyModelViewSet):
    """
    List search country model
    """
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = CountryStatsSerializer
    pagination_class = Pagination
    queryset = CountryCases.objects.all().order_by("-total_cases")
    filter_backends = (SearchFilter,)
    search_fields = ('country',)
    order_options = ['total_cases', 'new_cases', 'total_recovered',
                     'total_deaths', 'new_deaths',
                     'active_cases', 'serious_critical',
                     'cases_per_mill_pop']

    def search(self, request, *args, **kwargs):
        """
        search a country
        """
        setattr(self.request, 'last_update', GeneralStats.objects.all().order_by(
            '-created_at').first().last_update)
        print(
            f"\n\n\n\n[<<<<<<<{request.META.get('HTTP_REFERER', '') or request.headers.get('User-Agent', '')}>>>>>>>>>]\n\n\n\n")

        order, how = request.query_params.get(
            "order", None), request.query_params.get("how", None)
        if order:
            if order not in self.order_options:
                error_message = f"Invalid order options. Order options must be one of {self.order_options}"
                return Response({"errors": error_message}, status=status.HTTP_400_BAD_REQUEST)
            order = order if how == 'asc' else '-'+order
            self.queryset = CountryCases.objects.all().order_by(order)
        return super().list(request, *args, **kwargs)


class FetchData(generics.GenericAPIView):

    renderer_classes = (RequestJSONRenderer,)
    swagger_schema = None

    def get(self, request):
        """
        Get the general stats
        """
        print(
            f"<<<<<<<{request.META.get('HTTP_REFERER', '') or request.headers.get('User-Agent', '')}>>>>>>>>>")
        fech_data.delay()
        return Response({"meassage": "Data update started"}, status=status.HTTP_200_OK)
