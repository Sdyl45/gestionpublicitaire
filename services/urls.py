from django.urls import path

from . import views
from .views import *
urlpatterns = [
 path("acceuil", views.index, name="index"),



 



path('list/campagnes', liste_campagnesView.as_view(), name='CampagneList'),
path('creer/', CreerCampagneView.as_view(), name='creer_campagne'),
path('camp/<pk>/modifier', modifierCampagneView.as_view(), name='modifCampagne'),
 path('Campdetail/<pk>/effacer', deletecampagneView.as_view(), name='Campdelete'),
 path('campagnedetail/<pk>', detailcampagneView.as_view(), name='campagnedetail'),

 path("AddRapport", views.RapportsCampViews, name="rapport"),



path('creer-publicite/', CreatePubliciteView.as_view(), name='publication'),
path('creer-publication/', views.CreatePublicationView, name='publications'),
path('list-pubs/', views.list_pubs, name='listPubs'),  # URL pour la liste des publicités
path('pub/<pk>/modifier',  modifierPubliciteView.as_view(), name='modifPub'),
 path('Pubdetail/<pk>/effacer', deletepubliciteView.as_view(), name='pubdelete'),
 path('publicitedetail/<pk>', detailPubliciteView.as_view(), name='publicitedetail'), 

 path('audiences/create/', CreateAudienceView.as_view(), name='create_audience'),
path('audiences/', views.audience_list, name='audience_list'),
path("paie", views.PaiementViews, name="paiement"),





path('locations/create/', views.create_location, name='create_location'),
path("chatter",views.ChatsViews, name="chat"),
path("profile",views.ProfileViews, name="profil")
]
