from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError
import requests
import environ
import os
from pathlib import Path


# Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

BASE_API_URL = "https://macandrio.pythonanywhere.com/api/v1/"
BASE_API_URL_local = "http://127.0.0.1:8000/api/v1/"

def index(request):
    return render(request, 'index.html')

#------------------------------------------------Listar--------------------------------------------------------------
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


#------------------------------------------------Formularios------------------------------------------------------------
def crear_cabecera():
    return {
        'Authorization': 'Bearer '+env("Admin"),
        "Content-Type": "application/json"
        }


def Aeropuerto_busqueda_simple(request):
    aeropuerto = []
    if request.GET:
        formulario = BusquedaAeropuertoForm(request.GET)
        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.get(
                BASE_API_URL_local + 'Aeropuerto/busqueda_simple',
                headers=headers,
                params={'textoBusqueda':formulario.data.get("textoBusqueda")}
            )
            aeropuerto = response.json()
            return render(request, 'Formularios/Aeropuerto/buscar.html',{"aeropuerto":aeropuerto})
        if("HTTP_REFERER" in request.META):
            return redirect(request.META["HTTP_REFERER"])
        else:
            return redirect("index")

    else:
        formulario = BusquedaAeropuertoForm()

    return render(request, 'Formularios/Aeropuerto/buscar.html',{"aeropuerto":aeropuerto})


def Aeropuerto_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaAeropuertoForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                BASE_API_URL_local + 'Aeropuerto/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                aeropuerto = response.json()
                return render(request, 'Formularios/Aeropuerto/busqueda_avanzada.html',{"aeropuerto":aeropuerto})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'Formularios/Aeropuerto/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaAeropuertoForm(None)
    return render(request, 'Formularios/Aeropuerto/busqueda_avanzada.html',{"formulario":formulario})

import base64

#------------------------------------------------------Páginas de Error-----------------------------------------------------------------------------


def index(request): 
    return render(request, 'index.html')
def mi_error_400(request,exception=None):
    return render(request,"errors/400.html",None,None,400)

def mi_error_403(request,exception=None):
    return render(request,"errors/403.html",None,None,403)

def mi_error_404(request,exception=None):
    return render(request,"errors/404.html",None,None,404)

def mi_error_500(request,exception=None):
    return render(request,"errors/500.html",None,None,500)

