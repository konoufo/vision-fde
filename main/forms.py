from django import forms
from .models import Image
# import cv2

class ImageForm(forms.ModelForm):
    """Form for the image model"""

    # def show(img_object):
    #     cv2.imshow("out", img_object)
    #     cv2.waitKey(0)

    class Meta:
        model = Image
        fields = ('title', 'image')