from django.conf.urls import url, include
from rest_framework import routers
from imageupload_rest.viewsets import UploadImageViewset
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from imageupload_rest.viewsets import barcode

schema_view = get_schema_view(
    openapi.Info(
        title="API Vision",
        default_version='vFinal',
        description="Api pour gestion d'image",
        terms_of_service="https://yourco/terms/",
        contact=openapi.Contact(email="contact@images.remote"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "api_app"

router = routers.DefaultRouter()
router.register('images', UploadImageViewset, basename="api_page")
urlpatterns = [
    url('', include(router.urls)),
    url('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    url("redoc", schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]