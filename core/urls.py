
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('services.urls'), name='services'),
    path('', include('utilisateurs.urls'), name='utilisateurs'),
]
