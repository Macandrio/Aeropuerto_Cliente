Pasos a seguir al descargar el proyecto desde git

1. Nos situaremos en la crpeta Aeropuerto_Cliente
2. Crearemos la carpeta myven con:
    * python3 -m venv myvenv
3. Activaremos el entrono con:
    * source myvenv/bin/activate
4. Instalaremos los requirement y actualizaremos con:
    * python -m pip install --upgrade pip
    * pip install -r requirements.txt
5. Crearemos la base de datos con:
    * python manage.py makemigrations
    * python manage.py migrate