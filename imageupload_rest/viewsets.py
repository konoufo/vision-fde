import cv2
import numpy as np
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response

from imageupload_rest.serializers import  UploadImageSerializer
from imageupload.models import UploadImage
from rest_framework.decorators import action
from main import detect,barcode
from django.conf import settings
import os, cloudinary
import cloudinary.uploader

class UploadImageViewset(viewsets.ModelViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer

    @action(detail=True, methods=['post'])
    def reconImage(self, request, pk=None):
        response = {"status": "echec"}
        image = self.get_object()
        if image is not None:
            img = self.validate_image(image)
            # val = detect.mainproc(img_file=img)
            img_proc, Text, valeurs_nutritives, ingredients = detect.detect_VN_ING(img_file=img, fast=1)
            response = {'statut': 'success', 'Ingrédients': ingredients,'Valeurs nutritives': valeurs_nutritives}
            return Response(response)
        else:
            return Response({'statut': 'echec'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reconBarcode(self, request, pk=None):
        image = self.get_object()
        if image is not None:
            img = self.validate_image(image)
            code_barre = barcode.get_string_barcode(img_file=img)
            return Response(code_barre[3])
        else:
            return Response({'statut': 'echec'},
                            status=status.HTTP_400_BAD_REQUEST)
    def validate_image(self, image):
        image = cloudinary.CloudinaryImage(image.image_id)
        r = requests.get(image.url, stream=True)
        print(image.url)
        if r.ok:
            r.raw.decode_content = True
            file_bytes = np.asarray(bytearray(r.raw.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            return img
        return 0