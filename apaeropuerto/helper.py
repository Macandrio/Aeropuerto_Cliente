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
    
    def obtener_Aeropuerto(id):
        # obtenemos todos los Aeropuertos
        headers = {'Authorization': 'Bearer '+env("Admin")} 
        response = requests.get(BASE_API_URL + version + 'Aeropuerto/' + str(id) ,headers=headers)
        aeropuerto = response.json()
        return aeropuerto
