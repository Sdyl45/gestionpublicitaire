
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static

handler404='services.views.error_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('utilisateurs.urls'), name='utilisateurs'),
    path('', include('services.urls'), name='services'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)