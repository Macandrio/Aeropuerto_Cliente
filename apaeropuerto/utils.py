import xml.etree.ElementTree as ET
import requests
from requests.exceptions import HTTPError
from django.shortcuts import render

#---------------------------------------Manejar_Errores--------------------------------------------------------------

def manejar_errores_api(response, request, formulario=None, template="errors/error_general.html"):
    """
    Maneja los errores HTTP al hacer peticiones a la API REST.
    :param response: Respuesta de la API
    :param request: Objeto request de Django
    :param formulario: Formulario en caso de errores 400
    :param template: Plantilla para mostrar errores específicos
    :return: Render de la plantilla de error correspondiente
    """
    print(f"❌ Error HTTP: {response.status_code}")
    
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Hubo un error en la petición: {http_err}')
        
        if response.status_code == 400:
            errores = response.json()
            for error in errores:
                formulario.add_error(error, errores[error])
            
            return render(request, template, {"formulario": formulario, "errores": errores})
        
        return render(request, 'errors/500.html')

    if response.status_code == 401:
        return render(request, 'errors/401.html')  # Acceso no autorizado
    elif response.status_code == 403:
        return render(request, 'errors/403.html')  # Prohibido
    elif response.status_code == 404:
        return render(request, 'errors/404.html')  # No encontrado
    elif response.status_code >= 500:
        return render(request, 'errors/500.html')  # Error interno del servidor

    return render(request, template, {"error": "Ocurrió un error inesperado."})

def manejar_excepciones_api(err, request):
    """
    Maneja excepciones generales en las peticiones a la API.
    :param err: Excepción capturada
    :param request: Objeto request de Django
    :return: Render de la plantilla de error
    """
    print(f"⚠️ Error inesperado: {err}")
    
    if isinstance(err, requests.exceptions.RequestException):
        return render(request, 'errors/conexion_error.html')
    
    return render(request, 'errors/error_general.html')

#---------------------------------------Transformar_Respuesta--------------------------------------------------------------

def transformar_respuestas(response):
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        formato = response.json()
    elif "application/xml" in content_type:
        formato = ET.fromstring(response.text)
    else:
        formato = response.text
    return formato