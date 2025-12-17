from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Users app URLs
    path('users/', include('users.urls')),
    
    # Misc app URLs  
    path('misc/', include('misc.urls')),
    path('projects/',include('projects.urls'))
    # API docs (optional)
    # path('api-auth/', include('rest_framework.urls')),
]