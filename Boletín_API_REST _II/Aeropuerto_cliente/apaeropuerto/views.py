from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError
import requests
import environ
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from .utils import manejar_errores_api, manejar_excepciones_api  # Importar las funciones




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
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaAeropuertoForm(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    BASE_API_URL_local + 'Aeropuerto/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    aeropuerto = response.json()
                elif "application/xml" in content_type:
                    aeropuerto = ET.fromstring(response.text)  # Convertir XML a objeto
                else:
                    aeropuerto = response.text  # Si el formato es desconocido, tratarlo como texto

                print(" Datos recibidos:", aeropuerto)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Aeropuerto/busqueda_avanzada.html', {"aeropuerto": aeropuerto})
                else:
                    return manejar_errores_api(response, request, formulario, "Formularios/Aeropuerto/busqueda_avanzada.html")

            except Exception as err:
                return manejar_excepciones_api(err, request)
    else:
        formulario = BusquedaAvanzadaAeropuertoForm(None)

    return render(request, 'Formularios/Aeropuerto/busqueda_avanzada.html', {"formulario": formulario})


def Aerolinea_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaAerolineaForm(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    BASE_API_URL_local + 'Aerolinea/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    aerolinea = response.json()
                elif "application/xml" in content_type:
                    aerolinea = ET.fromstring(response.text)
                else:
                    aerolinea = response.text

                print(" Datos recibidos:", aerolinea)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Aerolinea/busqueda_avanzada.html', {"aerolinea": aerolinea})
                else:
                    return manejar_errores_api(response, request, formulario, "Formularios/Aerolinea/busqueda_avanzada.html")

            except Exception as err:
                return manejar_excepciones_api(err, request)
    else:
        formulario = BusquedaAvanzadaAerolineaForm(None)

    return render(request, 'Formularios/Aerolinea/busqueda_avanzada.html', {"formulario": formulario})


def Estadisticas_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaEstadisticas(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    BASE_API_URL_local + 'Estadisticas/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    estadisticas = response.json()
                elif "application/xml" in content_type:
                    estadisticas = ET.fromstring(response.text)
                else:
                    estadisticas = response.text

                print(" Datos recibidos:", estadisticas)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Estadisticas_vuelo/busqueda_avanzada.html', {"estadisticas": estadisticas})
                else:
                    return manejar_errores_api(response, request, formulario, "Formularios/Estadisticas_vuelo/busqueda_avanzada.html")

            except Exception as err:
                return manejar_excepciones_api(err, request)
    else:
        formulario = BusquedaAvanzadaEstadisticas(None)

    return render(request, 'Formularios/Estadisticas_vuelo/busqueda_avanzada.html', {"formulario": formulario})



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


