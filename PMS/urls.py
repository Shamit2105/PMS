from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('users/', include('users.urls')),
    
    path('misc/', include('misc.urls')),

    path('projects/',include('projects.urls')),

    path('tickets/',include("tickets.urls"))
    
]