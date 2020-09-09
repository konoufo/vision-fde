import os

from django.shortcuts import render
from . import detect
# Create your views here.
from django.http import HttpResponse

from .forms import ImageForm
import cv2
from . import detect
from django.conf import settings

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            im_name = form.cleaned_data['image'].name
            im_path = os.path.join(settings.MEDIA_ROOT,"images", im_name)

            #####call the algo
            img_proc = detect.process(im_path)
            im_name = "proc" + im_name
            img_proc_pathtosave = os.path.join(settings.STATIC_ROOT,"main", "img", im_name)
            print("XXXXXX path to save: ", img_proc_pathtosave,"XXXXXXXXXX")

            cv2.imwrite(img_proc_pathtosave, img_proc)
            # print(" XXXXXXXXXXXX ", form.cleaned_data['image'].name," XXXXXXXXXX ", im_path)

            return render(request, 'main/index.html', {'form': form, 'img_obj': img_obj, 'img_proc': img_proc_pathtosave})
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