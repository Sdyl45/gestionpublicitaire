from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CampagneForm, AudienceForm,LocationForm
from .models import Campagne, Audience,Location
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






def userViews(request):
 return render(request,'services/createUtilisateurs.html')
def listUserViews(request):
 return render(request,'services/listUtilisateurs.html')




def campaign_list(request):
 campaigns = Campagne.objects.all()
 return render(request, 'services/ListCampagne.html',locals())


def create_campaign(request):
 if request.method == 'POST':
  form = CampagneForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('CampagneList')
 else:
  form = CampagneForm()
 return render(request, 'services/MesCampagme.html', {'form': form})






def RapportsCampViews(request):
 return render(request,'services/CreerRapportsCampagne.html')




def AddPublicationViews(request):
 return render(request,'services/CreerPublication.html')

def ListPublicationViews(request):
 return render(request,'services/ListPubs.html')


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

def create_audience(request):
 if request.method == 'POST':
  audience_form = AudienceForm(request.POST)
  location_form = LocationForm(request.POST)
  if audience_form.is_valid() and location_form.is_valid():
   location = location_form.save()
   audience = audience_form.save(commit=False)
   audience.location = location
   audience.save()
   return redirect('audience_list')
 else:
  audience_form = AudienceForm()
  location_form = LocationForm()

 return render(request, 'services/CreerAudience.html', {'audience_form': audience_form, 'location_form': location_form})



def audience_list(request):
 audiences = Audience.objects.all()
 return render(request, 'services/audience_list.html',locals())



def PaiementViews(request):
 return render(request,'services/paiement.html')




def ChatsViews(request):
 return render(request,'services/chats.html')

def ProfileViews(request):
 return render(request,'services/profile.html')



