from django.urls import path, include
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions

schema_view_ = get_schema_view(
    openapi.Info(
        title="COVID19 Stats",
        default_version='v1',
        description="Free API documentation to get Real time corona virus stats"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
swagger_ui_view = get_swagger_view()



urlpatterns = [
    url(r'^docs/$', schema_view_.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view_.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^redoc/$', schema_view_.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^docs/$', swagger_ui_view),
    path('cases/', include('app.apis.cases.urls'))

]

