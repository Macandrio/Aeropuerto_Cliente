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
    
    textoBusqueda = forms.CharField(required=False)

    PAISES = [
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

    pais = forms.MultipleChoiceField(choices=PAISES,
                                required=False,
                                widget=forms.CheckboxSelectMultiple()
                               )
    ciudades = forms.MultipleChoiceField(choices=CIUDADES,
                                required=False,
                                widget=forms.CheckboxSelectMultiple()
                               )