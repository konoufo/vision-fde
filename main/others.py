#git filter-branch --force --index-filter "git rm --cached --ignore-unmatch main/Vision/ReconnaissanceDImages/yolov3_training_last.weights"  --prune-empty --tag-name-filter cat -- --all
import cv2
import numpy as np
import cloudinary.uploader
from main.Vision.ReconnaissanceDeTexte import detect
from io import BytesIO

def serializerTest():
    with open("produit02.jpg", "rb") as f:
        image = f
        image_stream = BytesIO(image.read())

    result = cloudinary.uploader.upload(image_stream)

    weigths = ["C:/Users/Erwin Anoh/PycharmProjects/weights/lait_du_canada.weights",
               "C:/Users/Erwin Anoh/PycharmProjects/weights/aliment_prepare_au_quebec.weights",
               "C:/Users/Erwin Anoh/PycharmProjects/weights/rain_fores.weights",
               ]
    cfgs = "main/Vision/ReconnaissanceDImages/yolov3_testing.cfg"

    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    data = img.tolist()
    a = np.array(data)

    var = img == a
    print(var.all(), "??")

    detect.detect_VN_ING(img_file=a, fast=0)