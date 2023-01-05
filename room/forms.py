from django.forms import ModelForm, Select
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class editRoom(ModelForm):
    class Meta:
        model = Room
        fields = ["capacity", "numberOfBeds", "roomType", "price"]

    widgets = {'roomType': Select(
        attrs={'class': "form-control w-100 p-2", 'placeholder': 'Room Type'})}


class editBooking(ModelForm):
    class Meta:
        model = Booking
        fields = ["startDate", "endDate"]


class editDependees(ModelForm):
    class Meta:
        model = Dependants
        fields = ["booking", "name"]
