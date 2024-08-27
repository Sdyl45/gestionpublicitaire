from django.urls import path

from . import views

urlpatterns = [
 path("", views.index, name="index"),



 path("Addutilisateurs", views.userViews, name="utilisateurs"),
 path("utilisateursList", views.listUserViews, name="Userlist"),


path('campagnes/', views.campaign_list, name='CampagneList'),
 path('campaigns/create/', views.create_campaign, name='campagne'),
 path("AddRapport", views.RapportsCampViews, name="rapport"),



path("AddPub", views.AddPublicationViews, name="publication"),
path("listPub", views.ListPublicationViews, name="listPubs"),




path('audiences/create/', views.create_audience, name='create_audience'),
path('audiences/', views.audience_list, name='audience_list'),
path("paie", views.PaiementViews, name="paiement"),





path('locations/create/', views.create_location, name='create_location'),
path("chatter",views.ChatsViews, name="chat"),
path("profile",views.ProfileViews, name="profil")
]
