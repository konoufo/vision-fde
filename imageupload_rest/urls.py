from django.conf.urls import url, include
from rest_framework import routers
from imageupload_rest.viewsets import UploadImageViewset
router = routers.DefaultRouter()
router.register('images', UploadImageViewset, 'images')
urlpatterns = [
    url('', include(router.urls))
]