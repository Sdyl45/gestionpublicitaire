from django.urls import path

from . import views
from .views import *
urlpatterns = [
 path("", views.index, name="index"),



 



path('list/campagnes', views.liste_campagnes, name='CampagneList'),
path('creer/', CreerCampagneView.as_view(), name='creer_campagne'),
 path("AddRapport", views.RapportsCampViews, name="rapport"),



path('creer-publicite/', CreatePubliciteView.as_view(), name='publication'),
path('list-pubs/', views.list_pubs, name='listPubs'),  # URL pour la liste des publicités





path('audiences/create/', CreateAudienceView.as_view(), name='create_audience'),
path('audiences/', views.audience_list, name='audience_list'),
path("paie", views.PaiementViews, name="paiement"),





path('locations/create/', views.create_location, name='create_location'),
path("chatter",views.ChatsViews, name="chat"),
path("profile",views.ProfileViews, name="profil")
]
