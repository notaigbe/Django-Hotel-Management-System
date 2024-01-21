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
        fields = ["brand", "drinkType", "price", "restock_level"]


class SalesForm(ModelForm):
    class Meta:
        model = Sales
        fields = ["item", "quantity"]
        widgets = {
            'item': Select(attrs={'class': 'form-control', 'placeholder': 'Drink', 'id': 'item', 'onchange':'updateSecondSelect()'}),
            'quantity': NumberInput(attrs={'class': "form-control w-100", 'placeholder': 'Quantity', 'id': 'quantity', 'min': '0'}),
        }


class OpeningStockForm(ModelForm):
    class Meta:
        model = Opening_Stock
        fields = ["item", "quantity"]

        widgets = {
            'item': Select(attrs={'class': 'form-control', 'placeholder': 'Drink', 'id': 'item'}),
            'quantity': NumberInput(attrs={'class': "form-control w-100", 'placeholder': 'Quantity', 'id': 'quantity'}),
        }


class RestockForm(ModelForm):
    class Meta:
        model = Restock
        fields = ["item", "quantity"]
        widgets = {
            'item': Select(attrs={'class': 'form-control', 'placeholder': 'Drink', 'id': 'item'}),
            'quantity': NumberInput(attrs={'class': "form-control w-100", 'placeholder': 'Quantity', 'id': 'quantity'}),
        }


class ClosingStockForm(ModelForm):
    class Meta:
        model = Closing_Stock
        fields = ["item", "quantity", "date"]
        widgets = {
            'item': Select(attrs={'class': 'form-control', 'placeholder': 'Drink', 'id': 'item'}),
            'quantity': NumberInput(attrs={'class': "form-control w-100", 'placeholder': 'Quantity', 'id': 'quantity'}),
        }
