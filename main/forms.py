from django import forms
from .models import Image
# import cv2

class ImageForm(forms.ModelForm):
    """Form for the image model"""

    # def show(img_object):
    #     cv2.imshow("out", img_object)
    # #     cv2.waitKey(0)
    # def __init__(self, *args, **kwargs):
    #     # first call parent's constructor
    #     super(ImageForm, self).__init__(*args, **kwargs)
    #     # # there's a `fields` property now
    #     self.fields['image'].required = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = True

    class Meta:
        model = Image
        fields = ('image',)
