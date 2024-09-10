from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.login, name='login'),
    path('user/logout', LogoutViews.as_view(), name='logout'),
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/List_register', views.listregisterView.as_view(), name='list_register'),
    path('user/<pk>/modifier', modifierUtilisateurView.as_view(), name='modifuser'),
    path('Userdetail/<pk>/effacer', deleteUserView.as_view(), name='userdelete'),

    path('user/forgot_password', views.forgot_password, name='forgot_password'),

]