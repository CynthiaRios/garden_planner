from django import forms
from .models import *

class UploadCropFileForm(forms.Form):
    crop_file = forms.FileField(required=False)
