import os

from django.shortcuts import render
from . import detect
# Create your views here.
from django.http import HttpResponse

from .forms import ImageForm
import cv2

from django.conf import settings

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            im_path = os.path.join(settings.MEDIA_ROOT,"images", form.cleaned_data['image'].name)

            # print(" XXXXXXXXXXXX ", form.cleaned_data['image'].name," XXXXXXXXXX ", im_path)

            ######################

            # import cv2
            # import pytesseract
            #
            #
            # #https://www.murtazahassan.com/courses/opencv-projects/
            # #control + left click
            # pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            #
            # # img = cv2.imread('D4\\main\\static\\main\\img\\produit01.jpg')
            # img = cv2.imread(im_path)
            #
            # #pytesseract only accept rgb, so we convert bgr to rgb
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #
            # ##Detecting characters and their position
            # #print(pytesseract.image_to_string(img))
            # ##character xpoint ypoint width heigth
            # #print(pytesseract.image_to_boxes(img))
            #
            # #taille
            # hImg, wImg,_ = img.shape
            # ##character xpoint ypoint width heigth
            # boxes = pytesseract.image_to_boxes(img)
            # for b in boxes.splitlines():
            #     print(b)
            #     b = b.split(' ')
            #     x,y,w,h = int( b[1]), int(b[2]), int(b[3]),int(b[4])
            #
            #     # cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 1)
            #     cv2.rectangle(img, (x,hImg - y), (w, hImg - h), (50, 50, 255), 2)
            #
            #     #ecrire le caracteres dessus
            #     cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 50), 2)
            #
            # cv2.imshow('reult', img)
            # cv2.waitKey(0)

            #########################

            return render(request, 'main/index.html', {'form': form, 'img_obj': img_obj})
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