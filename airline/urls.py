from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # aqui fica a parte dos admin a primeira url
    path('admin/', admin.site.urls),
    path('flights/', include('flights.urls')),
    path('users/', include('users.urls'))
]
