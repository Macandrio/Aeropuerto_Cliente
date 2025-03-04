# 📌 Usuarios de Prueba

| Tipo de Usuario	  | Nombre de Usuario	 | Contraseña |
|---------------------|----------------------|------------|
| Administrador       | admin                | admin      |
| Cliente             | Alejandro            | AGR12345   |
| Gerente             | Gerente              | AGR12345   |


# Tutorial de Uso de la Aplicación
Este tutorial está diseñado para que cualquier persona pueda desplegar y utilizar la aplicación de manera efectiva. Aquí se explican los pasos para desplegar la aplicación, así como cómo realizar las operaciones principales (GET, POST, PUT, DELETE, PATCH) utilizando el cliente.

# Requisitos Previos
Antes de comenzar, asegúrate de tener los siguientes requisitos:

Python 3.x: Necesario para correr el servidor.
Django: El framework utilizado para el backend.
Requests: Para hacer solicitudes HTTP al backend.
Un token de acceso válido: Necesitarás un token de autenticación para realizar las operaciones. Este token se obtiene después de iniciar sesión en la aplicación.



1. Desplegar la Aplicación

# Pasos para desplegar el servidor Django:

Clona el repositorio en tu máquina local.

    git clone <URL_DE_TU_REPOSITORIO>

Navega a la carpeta del proyecto.

    cd <nombre_del_proyecto>

Crea un entorno virtual e instálalo.

    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

Instala las dependencias necesarias.

    pip install -r requirements.txt

Realiza las migraciones de la base de datos.

    python manage.py migrate

Inicia el servidor de desarrollo de Django.

    python manage.py runserver

La aplicación estará corriendo en http://Macandiro.pyhonanywhere.com/.


2. Autenticación
Antes de realizar cualquier operación, necesitarás autenticarte y obtener un token de acceso. Para ello:

Realiza un POST a la URL de inicio de sesión para obtener el token.
Endpoint: POST http://Macandrio.pyhonanywhere.com/api/v1/login/

Cuerpo (Body):
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}

Respuesta: El servidor te devolverá un token de acceso que deberás usar para hacer las solicitudes siguientes.

3. Realizar Operaciones con el Cliente
    A continuación, se explica cómo realizar las operaciones más comunes con la API.

    3.1. Realizar una Solicitud GET
        El método GET se utiliza para obtener datos desde la API. Aquí te mostramos cómo obtener las reservas de un usuario autenticado.

    Asegúrate de tener un token de autenticación válido.
    Realiza un GET a la URL para listar las reservas.
        Endpoint: GET http://Macandrio.pyhonanywhere.com/api/v1//Reserva/pasajero
        Encabezados (Headers):
        Authorization: Bearer <tu_token>
        Respuesta: El servidor devolverá la lista de reservas del usuario autenticado en formato JSON.

    3.2. Realizar una Solicitud POST

    El método POST se utiliza para enviar datos al servidor y crear nuevos registros.

        Realiza un POST a la URL para crear una nueva reserva.
        Endpoint: POST http://Macandrio.pyhonanywhere.com/api/v1//Reserva/Crear/
        Encabezados (Headers):
        Authorization: Bearer <tu_token>
        Content-Type: application/json
        Cuerpo (Body):
        {
        "metodo_pago": tarjeta de credito,  [efectivo, paypal]
        "codigo_descuento": "Descuento15",
        "fecha_reserva": "2025-03-20T18:00:00",
        "estado": true,
        "vuelo": 4
        }
        Respuesta: El servidor devolverá los detalles de la reserva creada en formato JSON.

    3.3. Realizar una Solicitud PUT
    El método PUT se utiliza para actualizar un registro completo.

        Realiza un PUT a la URL para actualizar una reserva existente.
        Endpoint: PUT http://Macandrio.pyhonanywhere.com/api/v1/Reserva/editar/<id_reserva>/
        Encabezados (Headers):
        Authorization: Bearer <tu_token>
        Content-Type: application/json
        Cuerpo (Body):
        {
        "metodo_pago": efectivo,  [tarjeta de credito, paypal]
        "codigo_descuento": "Descuento15",
        "fecha_reserva": "2025-03-20T18:00:00",
        "estado": true,
        "vuelo": 4
        }
        Respuesta: El servidor devolverá los detalles de la reserva actualizada.

    3.4. Realizar una Solicitud DELETE
    El método DELETE se utiliza para eliminar un registro.

        Realiza un DELETE a la URL para eliminar una reserva existente.
        Endpoint: DELETE http://Macandrio.pyhonanywhere.com/api/v1/Reservas/eliminar/<id_reserva>/
        Encabezados (Headers):
        Authorization: Bearer <tu_token>
        Respuesta: El servidor devolverá un mensaje de confirmación de eliminación.

    3.5. Realizar una Solicitud PATCH
    El método PATCH se utiliza para actualizar parcialmente un registro.

        Realiza un PATCH a la URL para actualizar parcialmente una reserva.
        Endpoint: PATCH http://alvaroconde.pyhonanywhere.com/api/v1/Reservas/actualizar/codigo/<id_reserva>/
        Encabezados (Headers):
        Authorization: Bearer <tu_token>
        Content-Type: application/json
        Cuerpo (Body):
        {
        "codigo_descuento": "Descuento5"
        }
        Respuesta: El servidor devolverá los detalles de la reserva actualizada.


    4. Errores Comunes
    Al realizar operaciones, puedes encontrar algunos errores comunes que es importante saber cómo manejar:

        401 Unauthorized: Esto indica que no estás autenticado o que el token ha expirado.
        404 Not Found: La URL o el recurso solicitado no existe.
        400 Bad Request: Hay un error con los datos enviados al servidor (por ejemplo, formato incorrecto o falta de un campo obligatorio).

    Este es el flujo básico para interactuar con la API desde el cliente. Asegúrate de tener siempre un token válido y de utilizar las URLs y métodos HTTP correctos según la operación que desees realizar.