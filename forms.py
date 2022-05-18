from django.forms import ModelForm
from .models import Places
from django import forms

class PlacesForm(ModelForm):
    class Meta:
        model = Places
        fields = '__all__' #form that lists all model fields

