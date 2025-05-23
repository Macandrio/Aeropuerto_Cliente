import requests
import environ
import os
from pathlib import Path
from .utils import *  # Importar las funciones de errores

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

BASE_API_URL = env("BASE_API_URL")
version = env("version")
token = env("TOKEN_ACCESO")

class helper:

    def obtener_Aeropuertos():
        # obtenemos todos los Aeropuertos
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Aeropuerto/' ,headers=headers)
        aeropuertos = response.json()
        
        lista_aeropuertos = []
        for aeropuerto in aeropuertos:
            lista_aeropuertos.append((aeropuerto["id"],aeropuerto["nombre"]))
        return lista_aeropuertos
    
    def obtener_Aeropuerto(id):
        # obtenemos el Aeropuertos
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Aeropuerto/' + str(id) ,headers=headers)
        aeropuerto = response.json()
        return aeropuerto
    
    def obtener_Aerolinea(id):
        
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Aerolinea/' + str(id) ,headers=headers)
        aerolinea = response.json()
        return aerolinea

    def obtener_Pasajero_select():
        # obtenemos todos los Pasajeros
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Pasajeros/' ,headers=headers)
        pasajeros = response.json()
        
        lista_pasajeros = [("","Ninguna")]
        for pasajero in pasajeros:

            # Aquí tienes el ID del usuario
            usuario_id = pasajero["usuario"]
            response_usuario = requests.get(BASE_API_URL + version + 'Usuario/' + str(usuario_id) ,headers=headers)
            
            if response_usuario.status_code == 200:
                usuario_data = response_usuario.json()
                nombre_usuario = usuario_data.get("username", "Desconocido")  # Obtenemos el nombre de usuario
            else:
                nombre_usuario = "Desconocido"

            lista_pasajeros.append((pasajero["id"], nombre_usuario))
        return lista_pasajeros
    
    def obtener_Vuelos():
        # obtenemos todos los Aeropuertos
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Vuelos/' ,headers=headers)
        vuelos = response.json()
        
        lista_vuelos = [("","Ninguna")]
        for vuelo in vuelos:
            lista_vuelos.append((vuelo["id"],vuelo["id"]))
        return lista_vuelos
    
    def obtener_Vuelos_id(id):
        # obtenemos el Vuelo
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Vuelos/' + str(id) ,headers=headers)
        vuelo = response.json()
        return vuelo
    
    def obtener_Reserva(id):
        # obtenemos el Reserva
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Reserva/' + str(id) ,headers=headers)
        reserva = response.json()
        return reserva
    
    def obtener_Aerolineas():
        # obtenemos todos los Aerolineas
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Aerolineas/' ,headers=headers)
        aerolineas = response.json()
        
        lista_Aerolineas = [("","Ninguna")]
        for aerolinea in aerolineas:
            lista_Aerolineas.append((aerolinea["id"],aerolinea["id"]))
        return lista_Aerolineas
    
    def obtener_token_session(usuario,password):
        token_url = BASE_API_URL + '/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'mi_aplicacion',
            'client_secret': 'mi_aplicacion',
        }

        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))
        
    def obtener_Reservas_pasajero(id):
        # obtenemos el Reserva del pasajero
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Reserva/pasajero/' + str(id) ,headers=headers)
        reserva = response.json()
        return reserva
    
    def obtener_Equipaje_pasajero(id):
        # obtenemos el Reserva del pasajero
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Equipaje/pasajero/' + str(id) ,headers=headers)
        equipaje = response.json()
        return equipaje
    
    def obtener_vuelos_pasajero(id):
        # obtenemos el Vuelos del pasajero
        headers = {'Authorization': 'Bearer '+token} 
        response = requests.get(BASE_API_URL + version + 'Vuelo/pasajero/' + str(id) ,headers=headers)
        vuelo = response.json()
        return vuelo
    
    def obtener_usuario_actual_select(request):
        # 🔹 Verificar si el usuario está autenticado
        if "usuario" not in request.session:
            return [("", "Ninguna")]  # Si no está autenticado, devolver solo opción vacía

        usuario = request.session.get("usuario")  # 🔹 Obtener usuario logueado
        id_usuario = usuario.get("id")  # 🔹 Extraer ID del usuario autenticado

        headers = {'Authorization': 'Bearer ' + request.session.get("token")}
        
        # 🔹 Obtener solo el pasajero del usuario logueado desde la API
        response = requests.get(BASE_API_URL + version + 'Pasajeros/usuario/' + str(id_usuario), headers=headers)

        if response.status_code == 200:
            pasajeros = response.json()
            return pasajeros