from django import forms
from .models import *


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=100)
    file = forms.FileField()


class UpdatePriceForm(forms.Form):
    file = forms.FileField()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('description', 'file')


class MultiFileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))