from django.urls import path
from .views import *

urlpatterns = [
 path("", index, name="index"),



 path("Addutilisateurs", userViews, name="utilisateurs"),
 path("utilisateursList", listUserViews, name="Userlist"),



path("mesCampagnes", ListCampagneViews, name="CampagneList"),
 path("CampList", AddCampagneViews, name="campagne"),
 path("AddRapport", RapportsCampViews, name="rapport"),



path("AddPub", AddPublicationViews, name="publication"),
path("listPub", ListPublicationViews, name="listPubs"),



path("AddAudience", AudiencesViews, name="audience"),
path("paie", PaiementViews, name="paiement"),






path("chatter",ChatsViews, name="chat"),
path("profile",ProfileViews, name="profil")
]
