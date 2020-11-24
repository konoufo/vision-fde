from __future__ import absolute_import, unicode_literals
from io import BytesIO
from django.shortcuts import render
# Create your views here.

from .Vision.ReconnaissanceDImages import yolo_object_detection
from .forms import ImageForm
import cv2, cloudinary
import cloudinary.uploader
import numpy as np
from .Vision.ReconnaissanceDeTexte import detect
from .Vision.ReconnaissanceParCodeBarre import barcode


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST)

        image = request.FILES.get("image")
        image_stream = BytesIO(image.read())

        if form.is_valid():
            obj = form.save(commit=False)
            obj.image = None

            # Get the current instance object to display in the template
            var = request.POST.get("vision")
            result = cloudinary.uploader.upload(image_stream)
            obj.image_id = result["public_id"]
            obj.save()

            weigths = ["C:/Users/Erwin Anoh/PycharmProjects/weights/lait_du_canada.weights",
                        "C:/Users/Erwin Anoh/PycharmProjects/weights/aliment_prepare_au_quebec.weights",
                        "C:/Users/Erwin Anoh/PycharmProjects/weights/rain_fores.weights",
                       ]
            cfgs = "C:/Users/Erwin Anoh/PycharmProjects/D4/D4/main/Vision/ReconnaissanceDImages/yolov3_testing.cfg"

            image_stream.seek(0)
            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            ingredients = None
            valeurs_nutritives = None
            img_proc_datas = None
            fichier_json = 500*""
            barcode_str = None
            logos_detectes = []
            # img = pd.DataFrame(img).to_json('data.json', orient='split')
            if var == "barcode":
                # img: numpy.ndarray
                img_proc, barcode_str, text, fichier_json = barcode.get_string_barcode(img_file=img)

            else:
                s = 1
                v = request.POST.get("vitesse")
                if v == "non":
                    s = 0
                logo0, img_proc = yolo_object_detection.detect_logo(img_file=img, weigths=weigths[0],cfgs=cfgs, class_name="Lait du canada")
                logo1, img_proc = yolo_object_detection.detect_logo(img_file=img_proc, weigths=weigths[1],cfgs=cfgs, class_name="Aliment préparé au Québec")
                logo2, img_proc = yolo_object_detection.detect_logo(img_file=img_proc, weigths=weigths[2],cfgs=cfgs, class_name="Rain Forest Alliance")
            img_proc, Text, valeurs_nutritives, ingredients = detect.detect_VN_ING(img_file=img_proc, fast=s)
            logos_detectes.append(logo0)
            logos_detectes.append(logo1)
            logos_detectes.append(logo2)
            img_proc = cv2.imencode(".png", img_proc)[1].tobytes()
            result = cloudinary.uploader.upload(img_proc, public_id=obj.image_id + "proc", overwrite=True)
            image_proc_id = result["public_id"]

            #save the image processed to statics et the datas

            # ******************************
            # try:
            #     img_proc_datas_name = "data_" + image.name + ".txt"
            #     img_proc_datas_pathtosave = os.path.join(settings.STATIC_ROOT,"main", "datas", img_proc_datas_name)
            #
            #     # ******************************
            #     # with open(img_proc_datas_pathtosave, "w", encoding="utf-8") as file:
            #     #     for line in img_proc_datas:
            #     #         file.write(line + "\n")
            # except OSError:
            #     pass

            return render(request, 'main/index.html', {'form': form,
                                                       'img_obj': {"title": obj.title, "url": cloudinary.CloudinaryImage(obj.image_id).build_url()},
                                                       'img_proc': cloudinary.CloudinaryImage(image_proc_id).build_url(),
                                                       'img_proc_ingredients': ingredients,
                                                       'img_proc_valeurs_nutritives': valeurs_nutritives,
                                                       'img_proc_logos': logos_detectes,
                                                       'barcode_datas': fichier_json[0:500],
                                                       'radio': var,
                                                       'barcode_str': barcode_str,
                                                       })
    else:
        form = ImageForm()
    return render(request, 'main/index.html', {'form': form})
