import requests
from django.core import serializers
from django.shortcuts import render

import environ
import os
from pathlib import Path

# Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

BASE_API_URL = "https://macandrio.pythonanywhere.com/api/v1/"

def index(request):
    return render(request, 'index.html')

def aeropuerto_listar_api(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('PASAJERO')} 
        else:
            headers = {'Authorization': 'Bearer '+env('GERENTE')}
    else:
        headers = {'Authorization': 'Bearer '+env('PASAJERO')}


    response = requests.get(BASE_API_URL + 'Aeropuerto', headers=headers)
    aeropuertos = response.json()
    return render(request, 'paginas/aeropuerto_list.html', {"aeropuertos": aeropuertos})

def aerolinea_listar_api(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('PASAJERO')} 
        else:
            headers = {'Authorization': 'Bearer '+env('GERENTE')}
    else:
        headers = {'Authorization': 'Bearer '+env('PASAJERO')}
    response = requests.get(BASE_API_URL + 'Aerolinea', headers=headers)
    aerolineas = response.json()
    return render(request, 'paginas/aerolinea_list.html', {'aerolineas': aerolineas})


def vuelo_listar_api(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('PASAJERO')} 
        else:
            headers = {'Authorization': 'Bearer '+env('GERENTE')}
    else:
        headers = {'Authorization': 'Bearer '+env('PASAJERO')}
    response = requests.get(BASE_API_URL + 'Vuelo', headers=headers)
    vuelos = response.json()
    return render(request, 'paginas/vuelo_list.html', {'vuelos': vuelos})

def reserva_listar_api(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('PASAJERO')} 
        else:
            headers = {'Authorization': 'Bearer '+env('GERENTE')}
    else:
        headers = {'Authorization': 'Bearer '+env('PASAJERO')}
    response = requests.get(BASE_API_URL + 'Reserva', headers=headers)
    reservas = response.json()
    return render(request, 'paginas/reserva_list.html', {'reservas': reservas})


def vueloaerolinea_listar_api(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('PASAJERO')} 
        else:
            headers = {'Authorization': 'Bearer '+env('GERENTE')}
    else:
        headers = {'Authorization': 'Bearer '+env('PASAJERO')}
    response = requests.get(BASE_API_URL + 'Vueloaerolinea', headers=headers)
    vueloaerolinea = response.json()
    return render(request, 'paginas/vuelo_aerolinea_list.html', {'vueloaerolinea': vueloaerolinea})