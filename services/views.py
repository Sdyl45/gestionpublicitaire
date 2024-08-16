from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
 return render(request,'services/index.html')



# manage error page not found(404)

def error_404(request,exception):
 return render(request,'services/404.html',status=404)






def userViews(request):
 return render(request,'services/createUtilisateurs.html')
def listUserViews(request):
 return render(request,'services/listUtilisateurs.html')



def ListCampagneViews(request):
 return render(request,'services/ListCampagne.html')
def AddCampagneViews(request):
 return render(request,'services/MesCampagme.html')
def RapportsCampViews(request):
 return render(request,'services/CreerRapportsCampagne.html')




def AddPublicationViews(request):
 return render(request,'services/CreerPublication.html')

def ListPublicationViews(request):
 return render(request,'services/ListPubs.html')





def AudiencesViews(request):
 return render(request,'services/CreerAudience.html')


def PaiementViews(request):
 return render(request,'services/paiement.html')




def ChatsViews(request):
 return render(request,'services/chats.html')

def ProfileViews(request):
 return render(request,'services/profile.html')



