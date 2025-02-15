from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Aeropuerto/', views.aeropuerto_listar_api, name='aeropuerto_listar_api'),
    path('Aerolinea/', views.aerolinea_listar_api, name='aerolinea_listar_api'),
    path('Vuelo/', views.vuelo_listar_api, name='vuelo_listar_api'),
    path('Reserva/', views.reserva_listar_api, name='reserva_listar_api'),
    path('VueloAerolinea/', views.vueloaerolinea_listar_api, name='vueloaerolinea_listar_api'),

    #Mostrar 1
    path('Aeropeurto/<int:aeropuerto_id>',views.Aeropuerto_obtener, name='mostrar_aeropuerto'),


    #Buscar
    path('Aeropuerto/busqueda_simple/', views.Aeropuerto_busqueda_simple, name='Aeropuerto_busqueda_simple'),
    path('Aeropuerto/busqueda_avanzada/', views.Aeropuerto_busqueda_avanzada, name='Aeropuerto_busqueda_avanzada'),
    path('Aerolinea/busqueda_avanzada/', views.Aerolinea_busqueda_avanzada, name='Aerolinea_busqueda_avanzada'),
    path('Estadisticas/busqueda_avanzada/', views.Estadisticas_busqueda_avanzada, name='Estadisticas_busqueda_avanzada'),
    path('Reservas/busqueda_avanzada/', views.Reserva_busqueda_avanzada, name='Reserva_busqueda_avanzada'),


    #Crear
    path('Aeropuerto/Crear/', views.Aeropuerto_crear, name='Aeropuerto_crear'),


    #Editar
    path('aeropuerto/editar/<int:aeropuerto_id>/', views.aeropuerto_editar, name="aeropuerto_editar"),
]