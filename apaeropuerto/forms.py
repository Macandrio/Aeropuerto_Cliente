from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
#Aeropuerto

class BusquedaAeropuertoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True,widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre...',
            }))


class BusquedaAvanzadaAeropuertoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False,widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre...',
            }))

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

    pais = forms.MultipleChoiceField(
    choices=PAISES,
    required=False,
    widget=forms.CheckboxSelectMultiple(
        attrs={
            'class': 'custom-checkbox-group d-flex flex-wrap gap-2 p-2 border rounded bg-light'
        }
        )
    )

    ciudades = forms.MultipleChoiceField(choices=CIUDADES,
                                required=False,
                                widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'custom-checkbox-group d-flex flex-wrap gap-2 p-2 border rounded bg-light'
        }
        )
                               )
    

from django import forms

class BusquedaAvanzadaAerolineaForm(forms.Form):

    paises = [
        ("", "Seleccione un país"),  # Opción vacía por defecto
        ("ES", "España"),
        ("EN", "Inglaterra"),
        ("FR", "Francia"),
        ("IT", "Italia"),
    ]

    nombre = forms.CharField(
        required=False,
        label="Nombre de la aerolínea",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre de la aerolínea',
        })
    )

    codigo = forms.CharField(
        required=False,
        label="Código del Aeropuerto",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: MAD',
        })
    )

    fecha_fundacion = forms.DateField(
        required=False,
        label="Fecha de Fundación",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )

    pais = forms.ChoiceField(
        choices=paises,
        required=False,
        label="País",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )



class BusquedaAvanzadaEstadisticas(forms.Form):
    
    fecha_estadisticas = forms.DateField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fecha y Hora',
            'type' : 'date'
        })
    )

    numero_asientos_vendidos = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contenido...',
        })
    )

    numero_cancelaciones = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contenido...',
        })
    )

    feedback_pasajeros = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contenido...',
            })
        )

    

class BusquedaAvanzadaReserva(forms.Form):
    
    METODO_PAGO_CHOICES = [
        ('' , 'Elija uno metodo de pago'),
        ('tarjeta', 'Tarjeta de crédito'),
        ('efectivo', 'Efectivo'),
        ('paypal', 'PayPal'),
    ]

    metodo_pago = forms.ChoiceField(choices=METODO_PAGO_CHOICES,required=False)
    
    fecha_reserva = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fecha y Hora',
            'type' : 'date'
        })
    )

    estado_de_pago = forms.BooleanField(required=False,)
