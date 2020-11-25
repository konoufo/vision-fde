import os

import cv2
import numpy as np
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response

from D4 import settings
from imageupload_rest.serializers import UploadImageSerializer
from imageupload.models import UploadImage
from rest_framework.decorators import action
from main.Vision.ReconnaissanceDImages import yolo_object_detection
from main.Vision.ReconnaissanceDeTexte import detect
from main.Vision.ReconnaissanceParCodeBarre import barcode
import cloudinary
import cloudinary.uploader

class UploadImageViewset(viewsets.ModelViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer

    @action(detail=True, methods=['post'])
    def reconImage(self, request, pk=None):
        image = self.get_object()
        if image is not None:
            img = self.validate_image(image)

            logos_detectes = []
            weigths = [
                os.path.join(settings.WEIGHTS_ROOT, "lait_du_canada.weights"),
                os.path.join(settings.WEIGHTS_ROOT, "aliment_prepare_au_quebec.weights"),
                os.path.join(settings.WEIGHTS_ROOT, "rain_fores.weights")
            ]
            cfgs = "main/Vision/ReconnaissanceDImages/yolov3_testing.cfg"
            logo0, img_proc = yolo_object_detection.detect_logo(img_file=img,
                                                                weigths=weigths[0],
                                                                cfgs=cfgs,
                                                                class_name="Lait du canada")
            logo1, img_proc = yolo_object_detection.detect_logo(img_file=img,
                                                                weigths=weigths[1],
                                                                cfgs=cfgs,
                                                                class_name="Aliment préparé au Québec")
            logo2, img_proc = yolo_object_detection.detect_logo(img_file=img,
                                                                weigths=weigths[2],
                                                                cfgs=cfgs,
                                                                class_name="Rain Forest Alliance")
            logos_detectes.append(logo0)
            logos_detectes.append(logo1)
            logos_detectes.append(logo2)

            img_proc, Text, valeurs_nutritives, ingredients = detect.detect_VN_ING(img_file=img, fast=1)

            response = {'statut': 'success', 'Ingrédients': ingredients,'Valeurs nutritives': valeurs_nutritives, 'img_proc_logos': logos_detectes}

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'statut': 'echec'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reconBarcode(self, request, pk=None):
        image = self.get_object()
        if image is not None:
            img = self.validate_image(image)
            code_barre = barcode.get_string_barcode(img_file=img)
            return Response(code_barre[3], status=status.HTTP_200_OK)
        else:
            return Response({'statut': 'echec'}, status=status.HTTP_400_BAD_REQUEST)

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