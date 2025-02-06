from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apaeropuerto.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]


handler400="apaeropuerto.views.mi_error_400"
handler403="apaeropuerto.views.mi_error_403"
handler404="apaeropuerto.views.mi_error_404"
handler500="apaeropuerto.views.mi_error_500"