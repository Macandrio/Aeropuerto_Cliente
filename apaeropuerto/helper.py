import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

BASE_API_URL = env("BASE_API_URL")
version = env("version")

class helper:

    def obtener_Aeropuertos():
        # obtenemos todos los Aeropuertos
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Aeropuerto/' ,headers=headers)
        aeropuertos = response.json()
        
        lista_aeropuertos = []
        for aeropuerto in aeropuertos:
            lista_aeropuertos.append((aeropuerto["id"],aeropuerto["nombre"]))
        return lista_aeropuertos
    
    def obtener_Aeropuerto(id):
        # obtenemos el Aeropuertos
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Aeropuerto/' + str(id) ,headers=headers)
        aeropuerto = response.json()
        return aeropuerto
    
    def obtener_Aerolinea(id):
        
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Aerolinea/' + str(id) ,headers=headers)
        aerolinea = response.json()
        return aerolinea

    def obtener_Pasajero_select():
        # obtenemos todos los Pasajeros
        headers = {'Authorization': 'Bearer '+env("Admin")} 
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
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Vuelos/' ,headers=headers)
        vuelos = response.json()
        
        lista_vuelos = [("","Ninguna")]
        for vuelo in vuelos:
            lista_vuelos.append((vuelo["id"],vuelo["id"]))
        return lista_vuelos
    
    def obtener_Reserva(id):
        # obtenemos el Reserva
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Reserva/' + str(id) ,headers=headers)
        reserva = response.json()
        return reserva
    
    def obtener_Aerolineas():
        # obtenemos todos los Aerolineas
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Aerolineas/' ,headers=headers)
        aerolineas = response.json()
        
        lista_Aerolineas = [("","Ninguna")]
        for aerolinea in aerolineas:
            lista_Aerolineas.append((aerolinea["id"],aerolinea["id"]))
        return lista_Aerolineas