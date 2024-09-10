from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,EditUserForm
from django.contrib.auth import login as auth_login, authenticate,logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages  # Importez le module messages
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView,View
from .models import Utilisateur
from django.urls import reverse_lazy

# Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Connexion de l'utilisateur
            return redirect('index')  # Redirigez vers la page d'accueil ou une autre page
            messages.success(request, 'Connexion réussie !')  # Message de succès

        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'utilisateurs/login.html')





# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'utilisateurs/register.html', {'form': form})


# def listregister(request):
#  utilisateurs = Utilisateur.objects.all()
#  return render(request, 'utilisateurs/listUtilisateurs.html', locals())

class listregisterView(ListView):
    template_name = 'utilisateurs/listUtilisateurs.html'
    model = Utilisateur
    context_object_name = 'utilisateurs'
    login_url = reverse_lazy('register')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context= super().get_context_data(object_list=object_list,**kwargs)
        context['message']='papa mange'
        return context
    def test_func(self):
        return self.request.user.is_superuser
class RegisterView(CreateView):
    template_name = 'utilisateurs/register.html'
    model = Utilisateur
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')



    
class modifierUtilisateurView(UpdateView):    
    template_name = 'utilisateurs/register.html'
    model = Utilisateur
    form_class = EditUserForm
    success_url = reverse_lazy('list_register')


class deleteUserView(DeleteView):
    template_name = 'services/dropPub.html'
    model = Utilisateur
    context_object_name = 'utilisateur'
    success_url = reverse_lazy('list_register')
def forgot_password(request):
    return render(request, 'utilisateurs/forgot-password.html')



class LogoutViews(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Déconnexion réussie !')
        return redirect('login')

    def get(self, request):
        # Rediriger les requêtes GET vers la méthode POST
        return self.post(request)



