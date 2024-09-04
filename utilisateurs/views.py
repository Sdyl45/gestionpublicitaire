from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate,logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages  # Importez le module messages

# Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Renommez pour éviter les conflits
            messages.success(request, 'Connexion réussie !')  # Message de succès
            return redirect('index')  # Redirigez vers la page d'accueil ou une autre page
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'utilisateurs/login.html')





def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'utilisateurs/register.html', {'form': form})



def forgot_password(request):
    return render(request, 'utilisateurs/forgot-password.html')


def LogoutViews(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'utilisateurs/login.html')


