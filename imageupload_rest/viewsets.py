from rest_framework import viewsets, status
from rest_framework.response import Response

from imageupload_rest.serializers import  UploadImageSerializer
from imageupload.models import UploadImage
from rest_framework.decorators import action
from main import detect
from django.conf import settings
import os

class UploadImageViewset(viewsets.ModelViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer

    @action(detail=True, methods=['post'])
    def reconImage(self, request, pk=None):
        image = self.get_object()
        if image is not None:
            val = detect.mainproc(os.path.join(settings.MEDIA_ROOT, image.image.name))
            return Response({'statut': 'success', 'ingredients': val[0],'valeurs nutritives': val[1]})
        else:
            return Response({'statut': 'echec'},
                            status=status.HTTP_400_BAD_REQUEST)