from django.urls import path

from . import views
from .views import *
urlpatterns = [
 path("acceuil", views.index, name="index"),



 



path('list/campagnes', liste_campagnesView.as_view(), name='CampagneList'),
path('creer/', CreerCampagneView.as_view(), name='creer_campagne'),
path('camp/<int:pk>/modifier', modifierCampagneView.as_view(), name='modifCampagne'),
 path('Campdetail/<pk>/effacer', deletecampagneView.as_view(), name='Campdelete'),
 path('campagnedetail/<pk>', detailcampagneView.as_view(), name='campagnedetail'),

 path("AddRapport", views.RapportsCampViews, name="rapport"),



path('<int:pk>/creer-publicite/', CreatePubliciteView.as_view(), name='publication'),

path('publicites/', ListPubliciteView.as_view(), name='listPubs'),
path('pub/<pk>/modifier',  modifierPubliciteView.as_view(), name='modifPub'),
 path('Pubdetail/<pk>/effacer', deletepubliciteView.as_view(), name='pubdelete'),
 path('publicitedetail/<pk>', detailPubliciteView.as_view(), name='publicitedetail'),


path("paie", views.PaiementViews, name="paiement"),


path('publish/', PublishContentView.as_view(), name='publish_content'),
path('liste-posts/', ListPostsView.as_view(), name='liste_posts'),


path('locations/create/', views.create_location, name='create_location'),
path("chatter",views.ChatsViews, name="chat"),
path("profile",views.ProfileViews, name="profil"),




    path('audience/create/', CreateAudienceView.as_view(), name='create_audience'),
    path('audience/<int:pk>/edit/', UpdateAudienceView.as_view(), name='edit_audience'),
    path('audience/<int:pk>/delete/', DeleteAudienceView.as_view(), name='delete_audience'),
    path('audiences/', AudienceListView.as_view(), name='audience_list'),

    # URLs pour les localisations
    path('audience/<int:audience_id>/locations/', LocationListView.as_view(), name='location_list'),
    path('audience/<int:audience_id>/locations/add/', CreateLocationView.as_view(), name='add_location'),
    path('locations/<int:pk>/edit/', UpdateLocationView.as_view(), name='edit_location'),
    path('locations/<int:pk>/delete/', DeleteLocationView.as_view(), name='delete_location'),
    path("cond", views.accCondition, name="AccCondition"),
    path("condConf", views.accConditionConf, name="ConditionConf"),
]





