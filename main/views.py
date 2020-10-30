import os

from django.shortcuts import render
from . import detect
# Create your views here.
from django.http import HttpResponse

from .forms import ImageForm
import cv2
from . import detect, barcode
from django.conf import settings


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            var = request.POST.get("vision")
           # print("XXX Varr:", var)

            img_obj = form.instance
            im_name = form.cleaned_data['image'].name
            im_path = os.path.join(settings.MEDIA_ROOT,"images", im_name)

            im_name = "proc_" + im_name
            img_proc_pathtosave = os.path.join(settings.STATIC_ROOT_MAIN,"main", "img", im_name)

            if var == "barcode":
                img_proc, img_proc_datas, text, fichier_json = barcode.get_string_barcode(im_path)
                cv2.imwrite(img_proc_pathtosave, img_proc)
                #print(fichier_json)
            else:
                #####call the vision algo and extract image, image processed, image name and datas
                img_proc = detect.process(im_path)[0]
                img_proc_datas = detect.process(im_path)[1]
                #print("XXXXXX path to save: ", img_proc_pathtosave)

                #save the image processed to statics et the datas
                cv2.imwrite(img_proc_pathtosave, img_proc)

            img_proc_datas_name = "data_" + im_name + ".txt"
            img_proc_datas_pathtosave = os.path.join(settings.STATIC_ROOT_MAIN,"main", "datas", img_proc_datas_name)

            with open(img_proc_datas_pathtosave, "w", encoding="utf-8") as file:
                for line in img_proc_datas:
                    file.write(line + "\n")


            return render(request, 'main/index.html', {'form': form,
                                                       'img_obj': img_obj,
                                                       'img_proc': img_proc_pathtosave,
                                                       'img_proc_datas': img_proc_datas,
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