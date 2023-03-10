from django.forms import ModelForm, TextInput, NumberInput, Select
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *


class editFoodMenu(ModelForm):
    class Meta:
        model = FoodMenu
        fields = ["menuItems", "startDate", "endDate"]


class editEvent(ModelForm):
    class Meta:
        model = Event
        fields = ["eventType", "location",
                  "startDate", "endDate", "explanation"]


class createEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["eventType", "location",
                  "startDate", "endDate", "explanation"]


class createAnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'


class createItem(ModelForm):
    class Meta:
        model = Storage
        fields = ["itemName", "itemType", "quantity"]


class DrinkForm(ModelForm):
    class Meta:
        model = Drink
        fields = ["brand", "drinkType", "quantity", "price"]


class SalesForm(ModelForm):
    class Meta:
        model = Sales
        fields = ["item", "amount", "quantity"]
        widgets = {
            'item': Select(attrs={'class': 'form-control', 'placeholder': 'Drink'}),
            'amount': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'quantity': NumberInput(attrs={'class': "form-control w-100", 'placeholder': 'Quantity'}),
        }
