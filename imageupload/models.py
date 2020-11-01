from django.db import models

# Create your models here.
class UploadImage(models.Model):
    image = models.ImageField('Uploaded Image', null=True)
    image_id = models.TextField(blank=True, null=True)
