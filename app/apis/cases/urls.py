from django.urls import path
from .views import (GeneralStatsAPIView, FetchData, ListSearchCountriesAPIView)


urlpatterns = [
    path('general-stats', GeneralStatsAPIView.as_view(), name='cases-general-stats'),
    path('countries-search', ListSearchCountriesAPIView.as_view({'get': 'search'}), name='cases-countries-search'),
    path('scrap-data', FetchData.as_view(), name='cases-scrap-data'),
]
