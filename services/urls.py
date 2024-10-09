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
path('afficher-publications/', afficher_publications, name='afficher_publications'),
path('like_publication/', like_publication, name='like_publication'),
path('edit-post/<str:pk>/', EditPostView.as_view(), name='edit_post'),  # Changement ici
path('delete_post/<pk>/effaccer', DeletePostView.as_view(), name='delete_post'),
path('publicationdetail/<str:pk>/',detailPublicationView.as_view(), name='publicationdetail'),
 path('check_publication_status/', views.check_publication_status, name='check_publication_status'),



path('send_reply_to_api/', send_reply_to_api, name='send_reply_to_api'),
path("profile",views.ProfileViews, name="profil"),



# URLs pour les audiences
path('audience/create/', CreateAudienceView.as_view(), name='create_audience'),
path('audience/<int:pk>/edit/', UpdateAudienceView.as_view(), name='edit_audience'),
path('audience/<int:pk>/delete/', DeleteAudienceView.as_view(), name='delete_audience'),
path('audiences/', AudienceListView.as_view(), name='audience_list'),

# URLs pour les localisations
path('locations/create/', views.create_location, name='create_location'),
path('audience/<int:audience_id>/locations/', LocationListView.as_view(), name='location_list'),
path('audience/<int:audience_id>/locations/add/', CreateLocationView.as_view(), name='add_location'),
path('locations/<int:pk>/edit/', UpdateLocationView.as_view(), name='edit_location'),
path('locations/<int:pk>/delete/', DeleteLocationView.as_view(), name='delete_location'),
path("cond", views.accCondition, name="AccCondition"),
path("condConf", views.accConditionConf, name="ConditionConf"),


# URLS POUR LES BOOSTS
path('boost/', BoostPostView.as_view(), name='boost_post'),
path('boosts/', BoostedPostListView.as_view(), name='boosted_post_list'),
path('boosts/', BoostedPostListView.as_view(), name='boosted_post_list'),
path('boosts/stop/<int:pk>/', StopBoostView.as_view(), name='stop_boost'),
path('boosts/delete/<int:pk>/', DeleteBoostView.as_view(), name='delete_boost'),




# path('reply-to-comment/', reply_to_comment, name='reply_to_comment'),
]





