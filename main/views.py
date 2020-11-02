import os
from io import BytesIO

from django.shortcuts import render
from . import detect
# Create your views here.
from django.http import HttpResponse

from .forms import ImageForm
import cv2, cloudinary
import cloudinary.uploader
import numpy as np
from . import detect, barcode
from django.conf import settings


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST)

        # ******************************
        image = request.FILES.get("image")
        # image_stream = None
        # try:
        image_stream = BytesIO(image.read())
        # except AttributeError:
        #     image_stream = []

        if form.is_valid():
            obj = form.save(commit=False)
            obj.image = None

            # Get the current instance object to display in the template
            var = request.POST.get("vision")
           # print("XXX Varr:", var)

            result = cloudinary.uploader.upload(image_stream)
            obj.image_id = result["public_id"]
            obj.save()

            #******************************
            # img_proc_pathtosave = os.path.join(settings.STATIC_ROOT,"main", "img", im_name)
            image_stream.seek(0)
            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            ingredients = None
            valeurs_nutritives = None
            img_proc_datas = None
            fichier_json = 500*""
            barcode_str = None
            if var == "barcode":
                img_proc, barcode_str, text, fichier_json = barcode.get_string_barcode(img_file=img)
                # barcode_datas = barcode_datas
            else:
                # img_proc, img_proc_datas, box = detect.process(img_file=img)
                #I get and write explicitely all arguments so its better to understand; but I only use just some of them
                ingredients, valeurs_nutritives, img, img1, img2, img3, img4 = detect.mainproc(img_file=img)
                img_proc_datas = ingredients
                img_proc = img4
            # ******************************
            # cv2.imwrite(img_proc_pathtosave, img_proc)
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
                                                       'img_obj':{"title": obj.title, "url": cloudinary.CloudinaryImage(obj.image_id).build_url()},
                                                       'img_proc': cloudinary.CloudinaryImage(image_proc_id).build_url(),
                                                       'img_proc_ingredients': ingredients,
                                                       'img_proc_valeurs_nutritives': valeurs_nutritives,
                                                       'barcode_datas': fichier_json[0:500],
                                                       'radio': var,
                                                       'barcode_str': barcode_str,
                                                       })
    else:
        form = ImageForm()
    return render(request, 'main/index.html', {'form': form})

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    context = {}
    return render(request, 'main/index.html', context)

def response(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    context = {}
    return render(request, 'main/response.html', context)