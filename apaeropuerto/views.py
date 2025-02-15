from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
import requests
import environ
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from .utils import *  # Importar las funciones
from .helper import *
from .cliente_api import *




# Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

BASE_API_URL = env("BASE_API_URL")
version = env("version")


def crear_cabecera():
    return {
        'Authorization': 'Bearer '+env("Admin"),
        "Content-Type": "application/json"
        }




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

    response = requests.get(BASE_API_URL + version + 'Aeropuerto', headers=headers)
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
    response = requests.get(BASE_API_URL + version + 'Aerolinea', headers=headers)
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
    response = requests.get(BASE_API_URL + version + 'Vuelo', headers=headers)
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
    response = requests.get(BASE_API_URL + version + 'Reserva', headers=headers)
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
    response = requests.get(BASE_API_URL + version + 'Vueloaerolinea', headers=headers)
    vueloaerolinea = response.json()
    return render(request, 'paginas/vuelo_aerolinea_list.html', {'vueloaerolinea': vueloaerolinea})


#------------------------------------------------Formularios Buscar-----------------------------------------------------------------------------

def Aeropuerto_busqueda_simple(request):
    aeropuerto = []
    if request.GET:
        formulario = BusquedaAeropuertoForm(request.GET)
        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.get(
                BASE_API_URL + version + 'Aeropuerto/busqueda_simple',
                headers=headers,
                params={'textoBusqueda':formulario.data.get("textoBusqueda")}
            )
            aeropuerto = response.json()
            return render(request, 'Formularios/Aeropuerto/buscar.html',{"aeropuerto":aeropuerto,"formulario": formulario})
        if("HTTP_REFERER" in request.META):
            return redirect(request.META["HTTP_REFERER"])
        else:
            return redirect("index")

    else:
        formulario = BusquedaAeropuertoForm()

    return render(request, 'Formularios/Aeropuerto/buscar.html',{"formulario": formulario})


def Aeropuerto_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaAeropuertoForm(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    BASE_API_URL + version + 'Aeropuerto/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                aeropuerto = transformar_respuestas(response)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Aeropuerto/busqueda_avanzada.html', {"aeropuerto": aeropuerto,"formulario": formulario})
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
                    BASE_API_URL + version + 'Aerolinea/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                aerolinea = transformar_respuestas(response)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Aerolinea/busqueda_avanzada.html', {"aerolinea": aerolinea,"formulario": formulario})
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
                    BASE_API_URL + version + 'Estadisticas/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                estadisticas = transformar_respuestas(response)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Estadisticas_vuelo/busqueda_avanzada.html', {"estadisticas": estadisticas,"formulario": formulario})
                else:
                    return manejar_errores_api(response, request, formulario, "Formularios/Estadisticas_vuelo/busqueda_avanzada.html")

            except Exception as err:
                return manejar_excepciones_api(err, request)
    else:
        formulario = BusquedaAvanzadaEstadisticas(None)

    return render(request, 'Formularios/Estadisticas_vuelo/busqueda_avanzada.html', {"formulario": formulario})


def Reserva_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaReserva(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    BASE_API_URL + version + 'Reservas/busqueda_avanzada',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                #  Detectar formato de respuesta (JSON o XML)
                reservas = transformar_respuestas(response)

                print(" Datos recibidos:", reservas)

                if response.status_code == requests.codes.ok:
                    return render(request, 'Formularios/Reservas/busqueda_avanzada.html', {"reservas": reservas,"formulario": formulario})
                else:
                    return manejar_errores_api(response, request, formulario, "Formularios/Reservas/busqueda_avanzada.html")

            except Exception as err:
                return manejar_excepciones_api(err, request)
    else:
        formulario = BusquedaAvanzadaReserva(None)

    return render(request, 'Formularios/Reservas/busqueda_avanzada.html', {"formulario": formulario})

#------------------------------------------------Formularios_Crear-----------------------------------------------------------------------------

def Aeropuerto_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = AeropuertoForm(request.POST)

            headers =  crear_cabecera()

            datos = formulario.data.copy()
            datos["nombre"] = request.POST.get("nombre")
            datos["ciudades"] = request.POST.get("ciudades")
            datos["pais"] = request.POST.get("pais")
            datos["capacidad_maxima"] = request.POST.get("capacidad_maxima")

            
            response = requests.post(
                BASE_API_URL + version +'Aeropuerto/Crear',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, response.json())  # ✅ Mostrar mensaje en la plantilla
                return redirect("aeropuerto_listar_api")
            else:
                return manejar_errores_api(response, request, formulario, "Formularios/Aeropuerto/create.html")

        except Exception as err:
            return manejar_excepciones_api(err, request)  
    else:
         formulario = AeropuertoForm(None)
    return render(request, 'Formularios/Aeropuerto/create.html',{"formulario":formulario})

def Aerolinea_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = AerolineaForm(request.POST)

            headers =  crear_cabecera()

            datos = formulario.data.copy()
            datos["aeropuerto"] = request.POST.getlist("aeropuerto")

            datos["nombre"] = request.POST.get("nombre")
            datos["codigo"] = request.POST.get("codigo")
            datos["fecha_fundacion"] = str(
                                            datetime.date(year=int(datos['fecha_fundacion_year']),
                                                        month=int(datos['fecha_fundacion_month']),
                                                        day=int(datos['fecha_fundacion_day']))
                                             )
            datos["pais"] = request.POST.get("pais")
            

            
            response = requests.post(
                BASE_API_URL + version +'Aerolinea/Crear',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, response.json())  # ✅ Mostrar mensaje en la plantilla
                return redirect("aerolinea_listar_api")
            else:
                return manejar_errores_api(response, request, formulario, "Formularios/Aerolinea/create.html")

        except Exception as err:
            return manejar_excepciones_api(err, request)  
    else:
         formulario = AerolineaForm(None)
    return render(request, 'Formularios/Aerolinea/create.html',{"formulario":formulario})

#------------------------------------------------Formularios_Obtener-----------------------------------------------------------------------------

def Aeropuerto_obtener(request,aeropuerto_id):
    aeropuertos = helper.obtener_Aeropuerto(aeropuerto_id)
    return render(request, 'Formularios/Aeropuerto/aeropuerto_mostrar.html',{"aeropuerto":aeropuertos})

def Aerolinea_obtener(request,aerolinea_id):
    aerolinea = helper.obtener_Aerolinea(aerolinea_id)
    return render(request, 'Formularios/Aerolinea/aerolinea_mostrar.html',{"aerolinea":aerolinea})


#------------------------------------------------Formularios_Editar-----------------------------------------------------------------------------


def aeropuerto_editar(request,aeropuerto_id):
   
    datosFormulario = None
    
    # ✅ Si el usuario envió datos (POST), se almacenan en `datosFormulario`
    if request.method == "POST":
        datosFormulario = request.POST 
    
    # ✅ Obtener los datos actuales del aeropuerto desde la API
    aeropuerto = helper.obtener_Aeropuerto(aeropuerto_id) 

    #Crear el Formulario con Datos Iniciales
    formulario = AeropuertoForm(datosFormulario,
            initial={
                'nombre': aeropuerto['nombre'],
                'ciudades': aeropuerto["ciudades"],
                'pais': aeropuerto['pais'],
                'capacidad_maxima': aeropuerto['capacidad_maxima'],
            }
    )

    # ✅ Si el usuario envió un formulario (POST), procesamos los datos
    if (request.method == "POST"):
        formulario = AeropuertoForm(request.POST)
        datos = request.POST.copy()
        
        

        #Enviar los Datos a la API REST
        cliente = cliente_api(
                                env("Admin"),
                                "PUT",
                                'Aeropuerto/editar/'+str(aeropuerto_id),
                                datos
                            )
        
        cliente.realizar_peticion_api()

        #Manejar la Respuesta de la API
        if(cliente.es_respuesta_correcta()):
            # ✅ Guardar el mensaje directamente como lo envía la API
            mensaje = cliente.datosRespuesta

            # ✅ Guardar mensaje en Django Messages
            messages.success(request, mensaje)

            return redirect("mostrar_aeropuerto",aeropuerto_id=aeropuerto_id)
        else:
            if(cliente.es_error_validacion_datos()):
                cliente.incluir_errores_formulario(formulario)
            else:
                return manejar_errores_api(request,cliente.codigoRespuesta)
    return render(request, 'Formularios/Aeropuerto/editar.html',{"formulario":formulario,"aeropuerto":aeropuerto})

def Aerolinea_editar(request,aerolinea_id):
   
    datosFormulario = None
    
    # ✅ Si el usuario envió datos (POST), se almacenan en `datosFormulario`
    if request.method == "POST":
        datosFormulario = request.POST 
    
    # ✅ Obtener los datos actuales del aeropuerto desde la API
    aerolinea = helper.obtener_Aerolinea(aerolinea_id) 

    #Crear el Formulario con Datos Iniciales
    formulario = AerolineaForm(datosFormulario,
            initial={
                #'campo': modelo[dato]
                'nombre': aerolinea['nombre'],
                'codigo': aerolinea["codigo"],
                'pais': aerolinea['pais'],
                'fecha_fundacion': aerolinea['fecha_fundacion'],
                #'campo: [bucle]'
                'aeropuerto': [aerop for aerop in aerolinea['aeropuerto']],
            }
    )

    # ✅ Si el usuario envió un formulario (POST), procesamos los datos
    if (request.method == "POST"):
        formulario = AerolineaForm(request.POST)
        datos = request.POST.copy()
        datos["aeropuerto"] = request.POST.getlist("aeropuerto") # Para transformarla en lista
        
        
        cliente = cliente_api(
                                env("Admin"),
                                "PUT",
                                'Aerolinea/editar/'+str(aerolinea_id),
                                datos
                            )
        
        cliente.realizar_peticion_api()

        #Manejar la Respuesta de la API
        if(cliente.es_respuesta_correcta()):
            # ✅ Guardar el mensaje directamente como lo envía la API
            mensaje = cliente.datosRespuesta

            # ✅ Guardar mensaje en Django Messages
            messages.success(request, mensaje)

            return redirect("mostrar_aerolinea",aerolinea_id=aerolinea_id)
        else:
            if(cliente.es_error_validacion_datos()):
                cliente.incluir_errores_formulario(formulario)
            else:
                return manejar_errores_api(request,cliente.codigoRespuesta)
    return render(request, 'Formularios/Aerolinea/editar.html',{"formulario":formulario,"aerolinea":aerolinea})

#------------------------------------------------Formularios_Actualizar----------------------------------------------------------------------

def Aeropuerto_actualizar_nombre(request,aeropuerto_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    aeropuerto = helper.obtener_Aeropuerto(aeropuerto_id)
    formulario = AeropuertoActualizarNombreForm(datosFormulario,
            initial={
                'nombre': aeropuerto['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = AeropuertoActualizarNombreForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()
            response = requests.patch(
                BASE_API_URL + version + 'Aeropuerto/actualizar/nombre/'+str(aeropuerto_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("mostrar_aeropuerto",aeropuerto_id=aeropuerto_id)
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
                            'Formularios/Aeropuerto/actualizar_nombre.html',
                            {"formulario":formulario,"aeropuerto":aeropuerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'Formularios/Aeropuerto/actualizar_nombre.html',{"formulario":formulario,"aeropuerto":aeropuerto})

def Aerolinea_actualizar_nombre(request,aerolinea_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    aerolinea = helper.obtener_Aerolinea(aerolinea_id)
    formulario = AerolineaActualizarNombreForm(datosFormulario,
            initial={
                'nombre': aerolinea['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = AerolineaActualizarNombreForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()
            response = requests.patch(
                BASE_API_URL + version + 'Aerolinea/actualizar/nombre/'+str(aerolinea_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("mostrar_aerolinea",aerolinea_id=aerolinea_id)
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
                            'Formularios/Aerolinea/actualizar_nombre.html',
                            {"formulario":formulario,"aerolinea":aerolinea})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'Formularios/Aerolinea/actualizar_nombre.html',{"formulario":formulario,"aerolinea":aerolinea})
#------------------------------------------------Formularios_Eliminar----------------------------------------------------------------------


def Aeropuerto_eliminar(request,aeropuerto_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
           BASE_API_URL + version + 'Aeropuerto/eliminar/'+str(aeropuerto_id),
            headers=headers,
        )

        if(response.status_code == requests.codes.ok):
            mensaje = response.text.strip()  # ✅ Extraer el mensaje de la API sin validaciones
            messages.success(request, mensaje)
            return redirect("aeropuerto_listar_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('aeropuerto_listar_api')

def Aerolinea_eliminar(request,aerolinea_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
           BASE_API_URL + version + 'Aerolinea/eliminar/'+str(aerolinea_id),
            headers=headers,
        )

        if(response.status_code == requests.codes.ok):
            mensaje = response.text.strip()  # ✅ Extraer el mensaje de la API sin validaciones
            messages.success(request, mensaje)
            return redirect("aerolinea_listar_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('aerolinea_listar_api')

#------------------------------------------------Páginas de Error-----------------------------------------------------------------------------



def mi_error_400(request,exception=None):
    return render(request,"errors/400.html",None,None,400)

def mi_error_403(request,exception=None):
    return render(request,"errors/403.html",None,None,403)

def mi_error_404(request,exception=None):
    return render(request,"errors/404.html",None,None,404)

def mi_error_500(request,exception=None):
    return render(request,"errors/500.html",None,None,500)


