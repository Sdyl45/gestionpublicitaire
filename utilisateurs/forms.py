from django import forms
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Utilisateur
        fields = ['username', 'role']



class EditUserForm(UserCreationForm):

    class Meta:
        model = Utilisateur
        fields = ['username', 'role']