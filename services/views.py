from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CampagneForm, AudienceForm,LocationForm,PubliciteForm
from .models import Campagne, Audience,Location,Publicite
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
# Create your views here.



def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return redirect('create_location')
    else:
        form = LocationForm()

    return render(request, 'Services/Localisation.html', locals())











def index(request):
 return render(request,'services/index.html')



# manage error page not found(404)

def error_404(request,exception):
 return render(request,'services/404.html',status=404)








# creation de campagnes views debut
def liste_campagnes(request):
 campagnes = Campagne.objects.all()
 return render(request, 'services/ListCampagne.html', {'campagnes': campagnes})


# def creer_campagne(LoginRequiredMixin,UserPassesTestMixin,ListView):
#  if request.method == 'POST':
#   form = CampagneForm(request.POST)
#   if form.is_valid():
#    form.save()  # Enregistrer la campagne dans la base de données
#    return redirect('CampagneList')  # Rediriger vers la liste des campagnes
#  else:
#   form = CampagneForm()
# 
#  return render(request, 'services/MesCampagme.html', {'form': form})

class CreerCampagneView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    template_name = 'services/MesCampagme.html'
    model = Campagne
    form_class = CampagneForm
    success_url = reverse_lazy('CampagneList')

def RapportsCampViews(request):
 return render(request,'services/CreerRapportsCampagne.html')

# creation de campagnes views fin

# creation de publicite views debut


# 
# def creer_publicite(request):
#     if request.method == 'POST':
#         form = PubliciteForm(request.POST, request.FILES)  # N'oubliez pas de gérer les fichiers
#         if form.is_valid():
#             form.save()  # Enregistrer la publicité dans la base de données
#             return redirect('listPubs')  # Redirigez vers une page de liste ou une autre page
#     else:
#         form = PubliciteForm()
# 
#     return render(request, 'services/CreerPublication.html', {'form': form})

# class CreatePubliciteViews(LoginRequiredMixin,UserPassesTestMixin, CreateView):


class CreatePubliciteView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    template_name = 'services/CreerPublication.html'
    model = Publicite
    form_class = PubliciteForm
    success_url = reverse_lazy('listPubs')

def list_pubs(request):
    publicites = Publicite.objects.all()  # Récupère toutes les publicités
    return render(request, 'services/ListPubs.html', {'publicites': publicites})
# creation de publicite views fin














# creation d'audiencemview debut


# def create_audience(request):
#  if request.method == 'POST':
#   form = AudienceForm(request.POST)
#   if form.is_valid():
#    audience = form.save()
#    return redirect('audience_list')
#  else:
#   form = AudienceForm()
#
#  return render(request, 'services/CreerAudience.html', locals())

# def create_audience(request):
#  if request.method == 'POST':
#   audience_form = AudienceForm(request.POST)
#   location_form = LocationForm(request.POST)
#   if audience_form.is_valid() and location_form.is_valid():
#    location = location_form.save()
#    audience = audience_form.save(commit=False)
#    audience.location = location
#    audience.save()
#    return redirect('audience_list')
#  else:
#   audience_form = AudienceForm()
#   location_form = LocationForm()
#
#  return render(request, 'services/CreerAudience.html', {'audience_form': audience_form, 'location_form': location_form})

class CreateAudienceView(CreateView):
    form_class = AudienceForm
    form_class = LocationForm
    template_name = 'services/CreerAudience.html'
    success_url = reverse_lazy('audience_list')

def audience_list(request):
 audiences = Audience.objects.all()
 return render(request, 'services/audience_list.html',locals())

# creation d'audiencemview fin

def PaiementViews(request):
 return render(request,'services/paiement.html')




def ChatsViews(request):
 return render(request,'services/chats.html')

def ProfileViews(request):
 return render(request,'services/profile.html')



