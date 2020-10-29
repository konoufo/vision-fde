from django.conf.urls import url, include
from rest_framework import routers
from imageupload_rest.viewsets import UploadImageViewset

app_name = "api_app"

router = routers.DefaultRouter()
router.register('images', UploadImageViewset, basename="api_page")
urlpatterns = [
    url('', include(router.urls))
]