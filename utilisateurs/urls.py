from django.urls import path
from .views import *
urlpatterns = [
    path('user/login', login, name='login'),
    path('user/register', register, name='register'),
    path('user/forgot_password', forgot_password, name='forgot_password'),

]