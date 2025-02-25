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

def vuelo_listar_api_botones(request):
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
    return render(request, 'Formularios/Vuelo/vuelo_list.html', {'vuelos': vuelos})

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

def Reserva_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = ReservaForm(request.POST)

            headers =  crear_cabecera()

            datos = formulario.data.copy()
            datos["metodo_pago"] = request.POST.get("metodo_pago")

            
            response = requests.post(
                BASE_API_URL + version +'Reserva/Crear',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, response.json())  # ✅ Mostrar mensaje en la plantilla
                return redirect("reserva_listar_api")
            else:
                return manejar_errores_api(response, request, formulario, "Formularios/Reservas/create.html")

        except Exception as err:
            return manejar_excepciones_api(err, request)  
    else:
         formulario = ReservaForm(None)
    return render(request, 'Formularios/Reservas/create.html',{"formulario":formulario})

def Vuelo_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = VueloForm(request.POST)

            headers =  crear_cabecera()

            datos = formulario.data.copy()
            datos["origen"] = request.POST.get("origen")
            datos["destino"] = request.POST.get("destino")
            datos["aerolinea"] = request.POST.getlist("aerolinea")
            datos['estado'] = True if datos.get('estado') == 'on' else False  # Convertir 'on' a True

            
            response = requests.post(
                BASE_API_URL + version +'Vuelo/Crear',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, response.json())  # ✅ Mostrar mensaje en la plantilla
                return redirect("vuelo_listar_api")
            else:
                return manejar_errores_api(response, request, formulario, "Formularios/Vuelo/create.html")

        except Exception as err:
            return manejar_excepciones_api(err, request)  
    else:
         formulario = VueloForm(None)
    return render(request, 'Formularios/Vuelo/create.html',{"formulario":formulario})

#------------------------------------------------Formularios_Obtener-----------------------------------------------------------------------------

def Aeropuerto_obtener(request,aeropuerto_id):
    aeropuertos = helper.obtener_Aeropuerto(aeropuerto_id)
    return render(request, 'Formularios/Aeropuerto/aeropuerto_mostrar.html',{"aeropuerto":aeropuertos})

def Aerolinea_obtener(request,aerolinea_id):
    aerolinea = helper.obtener_Aerolinea(aerolinea_id)
    return render(request, 'Formularios/Aerolinea/aerolinea_mostrar.html',{"aerolinea":aerolinea})

def Reserva_obtener(request,reserva_id):
    reserva = helper.obtener_Reserva(reserva_id)
    print(" Datos recibidos:", reserva)
    return render(request, 'Formularios/Reservas/reserva_mostrar.html',{"reserva":reserva})

def Vuelo_obtener(request,vuelo_id):
    vuelo = helper.obtener_Vuelos_id(vuelo_id)
    print(" Datos recibidos:", vuelo)
    return render(request, 'Formularios/Vuelo/vuelo_mostrar.html',{"vuelo":vuelo})


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

#ManyToOne
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

#ManyToMany
def Reserva_editar(request,reserva_id):
   
    datosFormulario = None
    
    # ✅ Si el usuario envió datos (POST), se almacenan en `datosFormulario`
    if request.method == "POST":
        datosFormulario = request.POST 
    
    # ✅ Obtener los datos actuales del aeropuerto desde la API
    reserva = helper.obtener_Reserva(reserva_id) 

    #Crear el Formulario con Datos Iniciales
    formulario = ReservaForm(datosFormulario,
            initial={
                #'campo': modelo[dato]
                'fecha_reserva': reserva['fecha_reserva'],
                'codigo_descueto': reserva["codigo_descueto"],
                'metodo_pago': reserva['metodo_pago'],
                'estado_de_pago': reserva['estado_de_pago'],
                'pasajero': reserva["pasajero"]["usuario"],
                'vuelo': reserva["vuelo"]["id"],
            }
    )

    # ✅ Si el usuario envió un formulario (POST), procesamos los datos
    if (request.method == "POST"):
        formulario = ReservaForm(request.POST)
        datos = request.POST.copy()
        
        
        cliente = cliente_api(
                                env("Admin"),
                                "PUT",
                                'Reserva/editar/'+str(reserva_id),
                                datos
                            )
        
        cliente.realizar_peticion_api()

        #Manejar la Respuesta de la API
        if(cliente.es_respuesta_correcta()):
            # ✅ Guardar el mensaje directamente como lo envía la API
            mensaje = cliente.datosRespuesta

            # ✅ Guardar mensaje en Django Messages
            messages.success(request, mensaje)

            return redirect("mostrar_reserva",reserva_id=reserva_id)
        else:
            if(cliente.es_error_validacion_datos()):
                cliente.incluir_errores_formulario(formulario)
            else:
                return manejar_errores_api(request,cliente.codigoRespuesta)
    return render(request, 'Formularios/Reservas/editar.html',{"formulario":formulario,"reserva":reserva})

#ManyToMany Tablaintermedia
def Vuelo_editar(request,vuelo_id):
   
    datosFormulario = None
    
    # ✅ Si el usuario envió datos (POST), se almacenan en `datosFormulario`
    if request.method == "POST":
        datosFormulario = request.POST 
    
    # ✅ Obtener los datos actuales del aeropuerto desde la API
    vuelo = helper.obtener_Vuelos_id(vuelo_id) 
    print("📩 DEBUG - vuelo['origen']:", vuelo["origen"])

    #Crear el Formulario con Datos Iniciales
    formulario = VueloForm(datosFormulario,
            initial={
                #'campo': modelo[dato]
                'hora_salida': vuelo['hora_salida'],
                'hora_llegada': vuelo["hora_llegada"],
                'estado': vuelo['estado'],
                'duracion': vuelo['duracion'],
                'origen': vuelo["origen"]["id"],
                'destino': vuelo["destino"]["id"],
                'aerolinea': [indice['id'] for indice in vuelo['aerolinea']]
            }
    )

    # ✅ Si el usuario envió un formulario (POST), procesamos los datos
    if (request.method == "POST"):
        formulario = VueloForm(request.POST)
        datos = request.POST.copy()
        datos["origen"] = request.POST.get("origen")
        datos["destino"] = request.POST.get("destino")
        datos["aerolinea"] = request.POST.getlist("aerolinea")
        datos['estado'] = True if datos.get('estado') == 'on' else False  # Convertir 'on' a True
        
        cliente = cliente_api(
                                env("Admin"),
                                "PUT",
                                'Vuelo/editar/'+str(vuelo_id),
                                datos
                            )
        
        cliente.realizar_peticion_api()
        print("📩 DEBUG - Datos enviados a la API:", datos)
        print("📩 DEBUG - Código de respuesta API:", cliente.codigoRespuesta)

        #Manejar la Respuesta de la API
        if(cliente.es_respuesta_correcta()):
            # ✅ Guardar el mensaje directamente como lo envía la API
            mensaje = cliente.datosRespuesta

            # ✅ Guardar mensaje en Django Messages
            messages.success(request, mensaje)

            return redirect("mostrar_vuelo",vuelo_id=vuelo_id)
        else:
            if(cliente.es_error_validacion_datos()):
                cliente.incluir_errores_formulario(formulario)
            else:
                return manejar_errores_api(request,cliente.codigoRespuesta)
    return render(request, 'Formularios/Vuelo/editar.html',{"formulario":formulario,"vuelo":vuelo})

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

def Reserva_actualizar_codigo_descuento(request,reserva_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    reserva = helper.obtener_Reserva(reserva_id)
    formulario = ReservaActualizarcodigoForm(datosFormulario,
            initial={
                'codigo_descueto': reserva['codigo_descueto'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ReservaActualizarcodigoForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()
            response = requests.patch(
                BASE_API_URL + version + 'Reserva/actualizar/codigo/'+str(reserva_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("mostrar_reserva",reserva_id=reserva_id)
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
                            'Formularios/Reservas/actualizar_codigo.html',
                            {"formulario":formulario,"reserva":reserva})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'Formularios/Reservas/actualizar_codigo.html',{"formulario":formulario,"reserva":reserva})

def Vuelo_actualizar_hora_llegada(request,vuelo_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    vuelo = helper.obtener_Vuelos_id(vuelo_id)
    formulario = VueloActualizarcodigoForm(datosFormulario,
            initial={
                'hora_llegada': vuelo['hora_llegada'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = VueloActualizarcodigoForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()
            response = requests.patch(
                BASE_API_URL + version + 'Vuelo/actualizar/hora_llegada/'+str(vuelo_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("mostrar_vuelo",vuelo_id=vuelo_id)
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
                            'Formularios/Vuelo/actualizar_estado.html',
                            {"formulario":formulario,"vuelo":vuelo})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'Formularios/Vuelo/actualizar_estado.html',{"formulario":formulario,"vuelo":vuelo})
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

def Reserva_eliminar(request,reserva_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
           BASE_API_URL + version + 'Reserva/eliminar/'+str(reserva_id),
            headers=headers,
        )

        if(response.status_code == requests.codes.ok):
            mensaje = response.text.strip()  # ✅ Extraer el mensaje de la API sin validaciones
            messages.success(request, mensaje)
            return redirect("reserva_listar_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('reserva_listar_api')

def Vuelo_eliminar(request,vuelo_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
           BASE_API_URL + version + 'Vuelo/eliminar/'+str(vuelo_id),
            headers=headers,
        )

        if(response.status_code == requests.codes.ok):
            mensaje = response.text.strip()  # ✅ Extraer el mensaje de la API sin validaciones
            messages.success(request, mensaje)
            return redirect("vuelo_listar_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('vuelo_listar_api')


#------------------------------------------------usuario-----------------------------------------------------------------------------

def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    BASE_API_URL + version + 'registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    redirect("index")
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
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

#------------------------------------------------Páginas de Error-----------------------------------------------------------------------------



def mi_error_400(request,exception=None):
    return render(request,"errors/400.html",None,None,400)

def mi_error_403(request,exception=None):
    return render(request,"errors/403.html",None,None,403)

def mi_error_404(request,exception=None):
    return render(request,"errors/404.html",None,None,404)

def mi_error_500(request,exception=None):
    return render(request,"errors/500.html",None,None,500)


