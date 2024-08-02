
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

handler404='services.views.error_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('services.urls'), name='services'),
    path('', include('utilisateurs.urls'), name='utilisateurs'),
]
