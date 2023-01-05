from django.forms import ModelForm, TextInput, Select, DateInput, EmailInput

from .models import Reservation


class reservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'phoneNumber', 'email', 'startDate', 'endDate', 'room']

    widgets = {
        'name': TextInput(attrs={'class': "form-control", 'placeholder': 'Name'}),
        'room': Select(
            attrs={'class': "form-control", 'id': 'room', 'height': 100,
                   'overflow': 'scroll'}),
        'startDate': DateInput(format='%Y-%m-%d',
                              attrs={'class': 'form-control', 'placeholder': 'Pick a date',
                                     'type': 'date'}),
        'endDate': DateInput(format='%Y-%m-%d',
                               attrs={'class': 'form-control', 'placeholder': 'Pick a date',
                                      'type': 'date'}),
        'phoneNumber': TextInput(attrs={'class': "form-control", 'placeholder': 'Phone number'}),

        'email': EmailInput(
            attrs={'class': "form-control", 'placeholder': 'Email'}),
        }