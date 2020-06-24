from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Anak
from django.contrib.auth.forms import UserCreationForm

class AnakForm(ModelForm):
    class Meta:
        model = Anak
        fields = '__all__'
        exclude = ['image_profile','user']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class accountForm(ModelForm):
    model = Anak
    fields = '__all__'
