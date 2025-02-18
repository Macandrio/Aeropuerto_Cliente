from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Aeropuerto/', views.aeropuerto_listar_api, name='aeropuerto_listar_api'),
    path('Aerolinea/', views.aerolinea_listar_api, name='aerolinea_listar_api'),
    path('Vuelo/', views.vuelo_listar_api, name='vuelo_listar_api'),
    path('Reserva/', views.reserva_listar_api, name='reserva_listar_api'),
    path('Vuelo/', views.vuelo_listar_api, name='vuelo_listar_api'),
    path('Vuelo/buscar', views.vuelo_listar_api_botones, name='vuelo_listar_api_botones'),

    #Mostrar por id
    path('Aeropeurto/<int:aeropuerto_id>',views.Aeropuerto_obtener, name='mostrar_aeropuerto'),
    path('Aerolinea/<int:aerolinea_id>',views.Aerolinea_obtener, name='mostrar_aerolinea'),
    path('Reserva/<int:reserva_id>',views.Reserva_obtener, name='mostrar_reserva'),
    path('Vuelo/<int:vuelo_id>',views.Vuelo_obtener, name='mostrar_vuelo'),


    #Buscar
    path('Aeropuerto/busqueda_simple/', views.Aeropuerto_busqueda_simple, name='Aeropuerto_busqueda_simple'),
    path('Aeropuerto/busqueda_avanzada/', views.Aeropuerto_busqueda_avanzada, name='Aeropuerto_busqueda_avanzada'),
    path('Aerolinea/busqueda_avanzada/', views.Aerolinea_busqueda_avanzada, name='Aerolinea_busqueda_avanzada'),
    path('Estadisticas/busqueda_avanzada/', views.Estadisticas_busqueda_avanzada, name='Estadisticas_busqueda_avanzada'),
    path('Reservas/busqueda_avanzada/', views.Reserva_busqueda_avanzada, name='Reserva_busqueda_avanzada'),


    #Crear
    path('Aeropuerto/Crear/', views.Aeropuerto_crear, name='Aeropuerto_crear'),
    path('Aerolinea/Crear/', views.Aerolinea_crear, name='Aerolinea_crear'),
    path('Reserva/Crear/', views.Reserva_crear, name='Reserva_crear'),
    path('Vuelo/Crear/', views.Vuelo_crear, name='Vuelo_crear'),
     


    #Editar
    path('aeropuerto/editar/<int:aeropuerto_id>/', views.aeropuerto_editar, name="aeropuerto_editar"),
    path('Aerolinea/editar/<int:aerolinea_id>/', views.Aerolinea_editar, name="Aerolinea_editar"),
    path('Reserva/editar/<int:reserva_id>/', views.Reserva_editar, name="Reserva_editar"),
    path('Vuelo/editar/<int:vuelo_id>/', views.Vuelo_editar, name="Vuelo_editar"),
    
    #Actualizar
    path('aeropuerto/actualizar/nombre/<int:aeropuerto_id>',views.Aeropuerto_actualizar_nombre,name='Aeropuerto_actualizar_nombre'),
    path('Aerolinea/actualizar/nombre/<int:aerolinea_id>',views.Aerolinea_actualizar_nombre,name='Aerolinea_actualizar_nombre'),
    path('Reserva/actualizar/codigo/<int:reserva_id>',views.Reserva_actualizar_codigo_descuento,name='Reserva_actualizar_codigo_descuento'),
    path('Vuelo/actualizar/codigo/<int:vuelo_id>',views.Vuelo_actualizar_hora_llegada,name='Vuelo_actualizar_hora_llegada'),

    #Borrar
    path('Aeropuerto/eliminar/<int:aeropuerto_id>',views.Aeropuerto_eliminar, name='Aeropuerto_eliminar'),
    path('Aerolinea/eliminar/<int:aerolinea_id>',views.Aerolinea_eliminar, name='Aerolinea_eliminar'),
    path('Reserva/eliminar/<int:reserva_id>',views.Reserva_eliminar, name='Reserva_eliminar'),
    path('Vuelo/eliminar/<int:vuelo_id>',views.Vuelo_eliminar, name='Vuelo_eliminar'),

]