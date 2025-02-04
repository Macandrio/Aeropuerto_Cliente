from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#Aeropuerto

class BusquedaAeropuertoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BusquedaAvanzadaAeropuertoForm(forms.Form):

    PAISES = [
    ("", "Ninguno"),
    ("ES", "España"),
    ("FR", "Francia"),
    ("IT", "Italia"),
    ("DE", "Alemania"),
    ("PT", "Portugal"),
    ("NL", "Países Bajos"),
    ("BE", "Bélgica"),
    ("SE", "Suecia"),
    ("AT", "Austria"),
    ("CH", "Suiza"),
    ]
    CIUDADES = [
    ("", "Ninguno"),
    ("ES", "Madrid"),
    ("FR", "París"),
    ("IT", "Roma"),
    ("DE", "Berlín"),
    ("PT", "Lisboa"),
    ("NL", "Ámsterdam"),
    ("BE", "Bruselas"),
    ("SE", "Estocolmo"),
    ("AT", "Viena"),
    ("CH", "Ginebra"),
    ]
    
    textoBusqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    ciudades = forms.ChoiceField(
        choices=CIUDADES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    pais = forms.ChoiceField(
        choices=PAISES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )