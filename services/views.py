from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.backends import django
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from core.api.createCampaign import create_campaign
from core.api.createPublicite import create_ad_set
from .forms import CampaignForm, AudienceForm,LocationForm,PubliciteForm,EditPudForm,EditCampagneForm,PostPublicationForm,BoostedPostForm
from .models import Campaign, Audience, Location, Publicite, PostPublication, BoostedPost, Comment, Like,FacebookPostInfo
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
import os
import requests
from django.views.generic import TemplateView
from django.contrib import messages
from .templates.services.recupLikeAndComment import get_facebook_post_info_from_db


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
# def liste_campagnes(request):
#  campagnes = Campagne.objects.all()
#  return render(request, 'services/ListCampagne.html', {'campagnes': campagnes})


class liste_campagnesView(LoginRequiredMixin,ListView):
    template_name = 'services/ListCampagne.html'
    model = Campaign
    context_object_name = 'campagnes'
    login_url = reverse_lazy('CampagneList')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['message'] = 'papa mange'
        return context

    def test_func(self):
        return self.request.user.is_superuser

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

# class CreerCampagneView(LoginRequiredMixin, CreateView):
#     template_name = 'services/MesCampagme.html'
#     model = Campagne
#     form_class = CampagneForm
#     success_url = reverse_lazy('CampagneList')

#
# ACCESS_TOKEN = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
# ACCOUNT_ID = 'act_1822221194968260'
#
# # Initialiser l'API
# FacebookAdsApi.init(access_token=ACCESS_TOKEN)
class CreerCampagneView(LoginRequiredMixin, CreateView):
    template_name = 'services/MesCampagme.html'
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy('CampagneList')

    def form_valid(self, form):
        try:
            # Tenter de créer la campagne sur Facebook
            facebook_id = create_campaign(form.cleaned_data.get('name'))
            if not facebook_id:
                form.add_error(None, "La création de la campagne a échoué.")
                return self.form_invalid(form)

            # Sauvegarder l'instance de campagne
            instance = form.save(commit=False)
            instance.facebookCampaign_ID = facebook_id
            instance.save()

            # Vérifier si l'utilisateur souhaite créer une publicité
            if form.cleaned_data.get('create_ad'):
                return redirect('publication')  # Remplacez par le nom de votre URL pour créer une publicité

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, f"Une erreur s'est produite : {str(e)}")
            return self.form_invalid(form)

class modifierCampagneView(LoginRequiredMixin,UpdateView):
    template_name = 'services/MesCampagme.html'
    model = Campaign
    form_class = EditCampagneForm
    success_url = reverse_lazy('CampagneList')


class deletecampagneView(LoginRequiredMixin,DeleteView):
    template_name = 'services/dropPub.html'
    model = Campaign
    context_object_name = 'campagne'
    success_url = reverse_lazy('CampagneList')



def RapportsCampViews(request):
 return render(request,'services/CreerRapportsCampagne.html')



class detailcampagneView(LoginRequiredMixin,DetailView):
    template_name = 'services/DetailCampagne.html'
    model = Campaign
    context_object_name = 'campagne'
# creation de campagnes views fin



class CreatePubliciteView(LoginRequiredMixin, CreateView):
    template_name = 'services/CreerPublication.html'
    model = Publicite
    form_class = PubliciteForm
    success_url = reverse_lazy('listPubs')

    def form_valid(self, form):
        campagne_id = self.kwargs.get('pk')

        # Vérification si la campagne existe
        try:
            campagne = Campaign.objects.get(pk=campagne_id)
        except Campaign.DoesNotExist:
            form.add_error(None, "La campagne demandée n'existe pas.")
            return self.form_invalid(form)

        # Récupérer les données du formulaire
        name = form.cleaned_data.get('name')
        budget_quotidien = form.cleaned_data.get('budget_quotidien')  # Assurez-vous que ce champ est dans votre formulaire

        if not budget_quotidien:
            form.add_error(None, "Le budget quotidien est obligatoire.")
            return self.form_invalid(form)

        # Créer l'ensemble de publicités
        ad_set_id = create_ad_set(int(campagne.facebookCampaign_ID), name, budget_quotidien)

        if ad_set_id is None:
            form.add_error(None, "Échec de la création de l'ensemble de publicités.")
            return self.form_invalid(form)

        # Sauvegarder l'objet Publicite
        instance = form.save(commit=False)
        instance.campaign = campagne
        instance.facebookCampaign_ID = ad_set_id
        instance.save()

        return super().form_valid(form)





class ListPubliciteView(LoginRequiredMixin,ListView):
    model = Audience
    template_name = 'services/ListPubs.html'
    context_object_name = 'publicites'
    def get_queryset(self):
        return Publicite.objects.all()



class modifierPubliciteView(LoginRequiredMixin,UpdateView):
    template_name = 'services/CreerPublication.html'
    model = Publicite
    form_class = EditPudForm
    success_url = reverse_lazy('listPubs')


class deletepubliciteView(LoginRequiredMixin,DeleteView):
    template_name = 'services/dropPub.html'
    model = Publicite
    context_object_name = 'publicite'
    success_url = reverse_lazy('listPubs')


class detailPubliciteView(LoginRequiredMixin,DetailView):
    template_name = 'services/DetailPublicite.html'
    model = Publicite
    context_object_name = 'publicite'



def CreatePublicationView(request):
 return render(request,'services/createPublication.html')
# creation de publicite views fin


class CreateAudienceView(LoginRequiredMixin,CreateView):
    model = Audience
    form_class = AudienceForm
    template_name = 'services/CreerAudience.html'
    success_url = reverse_lazy('audience_list')

    def form_valid(self, form):
        # Sauvegarder l'audience
        response = super().form_valid(form)
        # Associer les localisations sélectionnées à l'audience
        form.instance.locations.set(form.cleaned_data['locations'])
        return response


# Vue pour mettre à jour une audience existante
class UpdateAudienceView(LoginRequiredMixin,UpdateView):
    model = Audience
    form_class = AudienceForm
    template_name = 'services/CreerAudience.html'
    success_url = reverse_lazy('audience_list')

    def form_valid(self, form):
        # Sauvegarder l'audience
        response = super().form_valid(form)
        # Mettre à jour les localisations associées à l'audience
        form.instance.locations.set(form.cleaned_data['locations'])
        return response




# Vue pour afficher la liste des audiences
class AudienceListView(LoginRequiredMixin,ListView):
    model = Audience
    template_name = 'services/Audience_list.html'
    context_object_name = 'audiences'

    def get_queryset(self):
        return Location.objects.all()


# Vue pour supprimer une audience
class DeleteAudienceView(LoginRequiredMixin,DeleteView):
    model = Audience
    template_name = 'services/DeleteAudience.html'
    success_url = reverse_lazy('audience_list')


# create audience fin

# create localisation debut
class CreateLocationView(LoginRequiredMixin,CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'services/CreerLocation.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        form.instance.audience_id = self.kwargs['audience_id']  # Associe la localisation à une audience
        return super().form_valid(form)


# Vue pour mettre à jour une localisation existante
class UpdateLocationView(LoginRequiredMixin,UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'services/CreerLocation.html'
    success_url = reverse_lazy('location_list')


# Vue pour afficher la liste des localisations
class LocationListView(LoginRequiredMixin,ListView):
    model = Location
    template_name = 'services/LocationList.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return Location.objects.filter(audience_id=self.kwargs['audience_id'])


# Vue pour supprimer une localisation
class DeleteLocationView(DeleteView):
    model = Location
    template_name = 'services/DeleteLocation.html'
    success_url = reverse_lazy('location_list')

# creation d'audiencemview fin

def PaiementViews(request):
 return render(request,'services/paiement.html')




def ChatsViews(request):
 return render(request,'services/chats.html')

def ProfileViews(request):
 return render(request,'services/profile.html')



class ListPostsView(LoginRequiredMixin, TemplateView):
    """
    Vue Django pour lister et enregistrer les publications d'une page Facebook dans un DataTable et en base de données.
    """
    template_name = 'services/liste_posts.html'
    page_id = '434662436390612'  # ID de la page Facebook
    access_token = 'EAAHZAsb1umoIBOwiDlKriZAXVNBeIGiEmLGrD1DputhuvZBNGTBepaLToxBAVrfSznxskwC06Vjb08ELmwLKyZAEkLFTU3Hyhqrneety6bCL64C69j2y1FiEqbeJNlDpit3vWMA0imz1tnWkM3VmtBPcNUXd65ZCox1f6VezZBFWr0jKeWZCe5Kh75ZA44MReoTBpDbXU2ZC4USHZC5VZComryWxoXN'  # Jeton d'accès Facebook

    def get_context_data(self, **kwargs):
        """
        Ajoute les publications Facebook au contexte pour affichage dans le template.
        """
        context = super().get_context_data(**kwargs)

        # Appel API pour récupérer les publications Facebook
        posts = self.get_posts()

        # Ajouter les publications au contexte pour affichage dans le template
        context['posts'] = posts
        return context

    def get_posts(self):
        """
        Récupère les publications de la page Facebook via l'API, les enregistre en base de données,
        et renvoie une liste de publications.
        """
        get_posts_url = f'https://graph.facebook.com/v17.0/{self.page_id}/posts'
        get_posts_params = {
            'access_token': self.access_token
        }

        # Effectuer une requête GET pour récupérer les publications
        response = requests.get(get_posts_url, params=get_posts_params)

        if response.status_code == 200:
            # Traiter la réponse JSON de l'API
            info_post = response.json()
            posts = info_post.get('data', [])

            # Parcourir les publications et les enregistrer en base de données
            for post in posts:
                post_obj, created = PostPublication.objects.get_or_create(
                    id_publication=post.get('id'),  # Utiliser 'id' pour identifier la publication
                    defaults={
                        'post_type': post.get('type', ''),  # Utiliser 'type' pour définir le type de publication
                        'message': post.get('message', ''),  # Message de la publication
                        'description': post.get('story', ''),  # Story ou description
                        'created_at': post.get('created_time'),  # Date de création
                        'user': self.request.user  # Utilisateur actuel
                    }
                )

                # Log pour indiquer si la publication a été ajoutée ou déjà présente
                if created:
                    print(f"Publication {post_obj.id_publication} ajoutée à la base de données.")
                else:
                    print(f"Publication {post_obj.id_publication} déjà présente dans la base de données.")

                # Récupérer les likes et les commentaires
                self._fetch_likes(post_obj.id_publication)
                self._fetch_comments(post_obj.id_publication)

            return posts
        else:
            # En cas d'erreur lors de l'appel à l'API, afficher un message d'erreur
            print(f"Erreur lors de la récupération des publications: {response.status_code} - {response.json()}")
            return []

    def _fetch_likes(self, post_id):
        """
        Récupère les likes associés à une publication Facebook et les enregistre.
        """
        likes_url = f"https://graph.facebook.com/v17.0/{post_id}/likes"
        params = {
            'access_token': self.access_token
        }
        response = requests.get(likes_url, params=params)

        if response.status_code == 200:
            likes_data = response.json().get('data', [])
            post = PostPublication.objects.filter(id_publication=post_id).first()  # Récupérer la publication
            if post:  # Vérifiez si la publication existe
                for like in likes_data:
                    liker_id = like.get('id')
                    liker_name = like.get('name', 'Inconnu')

                    # Enregistrer le like dans la base de données
                    Like.objects.update_or_create(
                        liker_id=liker_id,
                        post=post,
                        defaults={'liker_name': liker_name}
                    )
            else:
                print(f"Publication avec id {post_id} non trouvée.")
        else:
            print(f"Erreur lors de la récupération des likes : {response.text}")

    def _fetch_comments(self, post_id):
        """
        Récupère les commentaires associés à une publication Facebook et les enregistre.
        """
        comments_url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
        params = {
            'access_token': self.access_token
        }
        response = requests.get(comments_url, params=params)

        if response.status_code == 200:
            comments_data = response.json().get('data', [])
            post = PostPublication.objects.filter(id_publication=post_id).first()  # Récupérer la publication
            if post:  # Vérifiez si la publication existe
                for comment in comments_data:
                    comment_id = comment.get('id')
                    message = comment.get('message', 'Aucun message')
                    commenter_name = comment.get('from', {}).get('name', 'Inconnu')
                    created_time = comment.get('created_time')

                    # Enregistrer le commentaire dans la base de données
                    Comment.objects.update_or_create(
                        comment_id=comment_id,
                        post=post,
                        defaults={
                            'message': message,
                            'commenter_name': commenter_name,
                            'created_time': created_time,
                        }
                    )
            else:
                print(f"Publication avec id {post_id} non trouvée.")
        else:
            print(f"Erreur lors de la récupération des commentaires : {response.text}")



class PublishContentView(LoginRequiredMixin, CreateView):
    model = PostPublication
    template_name = 'services/CreerPublication.html'
    form_class = PostPublicationForm
    success_url = reverse_lazy('liste_posts')

    # ID de la page Facebook et jeton d'accès
    page_id = '434662436390612'
    access_token = 'EAAHZAsb1umoIBOwiDlKriZAXVNBeIGiEmLGrD1DputhuvZBNGTBepaLToxBAVrfSznxskwC06Vjb08ELmwLKyZAEkLFTU3Hyhqrneety6bCL64C69j2y1FiEqbeJNlDpit3vWMA0imz1tnWkM3VmtBPcNUXd65ZCox1f6VezZBFWr0jKeWZCe5Kh75ZA44MReoTBpDbXU2ZC4USHZC5VZComryWxoXN'

    # Chemin vers le répertoire des images et vidéos
    media_directory = r'C:\Users\LYAN\PycharmProjects\GestionPublicitaire\static\images'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user

        # Publier le contenu sur Facebook
        response = self._publish_to_facebook(post)

        if 'error' in response:
            # Gérer l'erreur de publication
            form.add_error(None, f"Erreur lors de la publication sur Facebook: {response['error']}")
            return self.form_invalid(form)

        # Si la publication est réussie, sauvegarder l'ID de la publication Facebook
        post.id_publication = response.get('id')
        post.save()

        # Récupérer les commentaires et likes après la publication
        self._fetch_comments(post.id_publication)
        self._fetch_likes(post.id_publication)

        return super().form_valid(form)

    def _publish_to_facebook(self, post):
        """
        Publier un message, une image ou une vidéo sur Facebook en fonction du type de publication.
        """
        if post.post_type == 'message':
            return self._publish_message(post.message)
        elif post.post_type == 'image' and post.image:
            image_path = os.path.join(self.media_directory, os.path.basename(post.image.path))
            return self._publish_image(image_path, post.message)
        elif post.post_type == 'video' and post.video:
            video_path = os.path.join(self.media_directory, os.path.basename(post.video.path))
            return self._publish_video(video_path, post.description)
        else:
            return {"error": "Type de publication non pris en charge."}

    def _publish_message(self, message):
        """
        Publier un message simple sur le mur de la page Facebook.
        """
        post_url = f'https://graph.facebook.com/v17.0/{self.page_id}/feed'
        post_params = {
            'message': message,
            'access_token': self.access_token
        }
        response = requests.post(post_url, data=post_params)
        return self._handle_response(response)

    def _publish_image(self, image_path, message):
        """
        Publier une image avec un message sur le mur de la page Facebook.
        """
        post_url = f'https://graph.facebook.com/v17.0/{self.page_id}/photos'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                post_params = {
                    'access_token': self.access_token,
                    'message': message
                }
                files = {'source': image_file}
                response = requests.post(post_url, data=post_params, files=files)
            return self._handle_response(response)
        else:
            return {"error": f"Fichier image non trouvé à {image_path}."}

    def _publish_video(self, video_path, description):
        """
        Publier une vidéo avec une description sur le mur de la page Facebook.
        """
        post_url = f'https://graph.facebook.com/v17.0/{self.page_id}/videos'
        if os.path.exists(video_path):
            with open(video_path, 'rb') as video_file:
                post_params = {
                    'access_token': self.access_token,
                    'description': description
                }
                files = {'source': video_file}
                response = requests.post(post_url, data=post_params, files=files)
            return self._handle_response(response)
        else:
            return {"error": f"Fichier vidéo non trouvé à {video_path}."}

    def _handle_response(self, response):
        """
        Gérer les réponses de l'API Facebook. Retourne l'erreur ou le JSON de succès.
        """
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_message = response.json().get('error', {}).get('message', 'Unknown error')
            except ValueError:
                error_message = response.text
            return {
                "error": f"Échec de la publication. Code: {response.status_code}, Erreur: {error_message}"
            }

    def _fetch_comments(self, post_id):
        """
        Récupérer les commentaires associés à une publication Facebook et les enregistrer.
        """
        comments_url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
        params = {
            'access_token': self.access_token
        }
        response = requests.get(comments_url, params=params)

        if response.status_code == 200:
            comments_data = response.json().get('data', [])
            for comment in comments_data:
                comment_id = comment.get('id')
                message = comment.get('message', 'Aucun message')
                commenter_name = comment.get('from', {}).get('name', 'Inconnu')
                created_time = comment.get('created_time')

                # Enregistrer le commentaire dans la base de données
                Comment.objects.update_or_create(
                    comment_id=comment_id,
                    defaults={
                        'post': PostPublication.objects.get(id_publication=post_id),
                        'message': message,
                        'commenter_name': commenter_name,
                        'created_time': created_time,
                    }
                )
        else:
            print(f"Erreur lors de la récupération des commentaires : {response.text}")

    def _fetch_likes(self, post_id):
        """
        Récupérer les likes associés à une publication Facebook et les enregistrer.
        """
        likes_url = f"https://graph.facebook.com/v17.0/{post_id}/likes"
        params = {
            'access_token': self.access_token
        }
        response = requests.get(likes_url, params=params)

        if response.status_code == 200:
            likes_data = response.json().get('data', [])
            for like in likes_data:
                liker_name = like.get('name', 'Inconnu')

                # Enregistrer le like dans la base de données
                Like.objects.update_or_create(
                    post=PostPublication.objects.get(id_publication=post_id),
                    liker_name=liker_name
                )
        else:
            print(f"Erreur lors de la récupération des likes : {response.text}")


class EditPostView(LoginRequiredMixin, UpdateView):
    model = PostPublication
    template_name = 'services/edit_post.html'
    form_class = PostPublicationForm
    success_url = reverse_lazy('liste_posts')

    def get_object(self, queryset=None):
        # Utiliser get_object_or_404 pour obtenir la publication
        return get_object_or_404(PostPublication, id_publication=self.kwargs['pk'])


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = PostPublication
    template_name = 'services/confirm_delete.html'
    success_url = reverse_lazy('liste_posts')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'La publication a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# partie des publications fin


def accCondition(request):
    return render(request, 'services/acceuilConditionsConf.html')

def accConditionConf(request):
    """
    Vue pour la page des conditions de confidentialité.
    """
    return render(request, 'services/Aconfidentialite.html')









# function boost pub debut

ACCESS_TOKEN = 'EAAHZAsb1umoIBOZB76FM28YLQBchTu8YacXlo9ZCJRRIJULIO7FenyIVwHPc0VmT6ibFwMZBHksH9pZCKV7dxrUqBVnmCxobZCU7SKPGhZBKXkshYnVGCErOR4MkgfOuzvAfZC7By8whzdVszOlMfu96s7PByOc1IOasH0nTuyK4RwuZByNa7cSEjHCzXv8DKGlLMUdDDFQWoTZBZBhlgR513IshMiA'
ACCOUNT_ID = 'act_1822221194968260'

FacebookAdsApi.init(access_token=ACCESS_TOKEN)

class BoostPostView(LoginRequiredMixin,CreateView):
    model = BoostedPost
    template_name = 'services/boost_post.html'
    form_class = BoostedPostForm
    success_url = reverse_lazy('boosted_posts')

    def form_valid(self, form):
        # Récupérer la campagne active
        campaign = Campaign.objects.first()

        if not campaign:
            form.add_error(None, "Aucune campagne trouvée.")
            return self.form_invalid(form)

        post_id = form.cleaned_data['post_id']
        page_id = form.cleaned_data['434662436390612']

        # Créer un ensemble de publicités pour booster la publication
        ad_account = AdAccount(ACCOUNT_ID)
        ad_set = ad_account.create_ad_set(params={
            'name': 'Boost Publication Ad Set',
            'campaign_id': campaign.facebookCampaign_ID,
            'daily_budget': int(campaign.budget_quotidien * 100),  # en centimes
            'billing_event': 'IMPRESSIONS',
            'optimization_goal': 'POST_ENGAGEMENT',
            'targeting': {
                'geo_locations': {'countries': ['CM']},  # Ciblage du Cameroun
            },
            'status': 'PAUSED',
        })

        ad_set_id = ad_set['id']

        # Sauvegarder l'ensemble de publicités créé dans la base de données
        boosted_post = form.save(commit=False)
        boosted_post.campaign = campaign
        boosted_post.ad_set_id = ad_set_id
        boosted_post.save()

        return super().form_valid(form)






class BoostedPostListView(LoginRequiredMixin,ListView):
    model = BoostedPost
    template_name = 'services/boosted_post_list.html'
    context_object_name = 'boosted_posts'

class StopBoostView(LoginRequiredMixin,View):
    def post(self, request, pk):
        boosted_post = get_object_or_404(BoostedPost, pk=pk)
        boosted_post.stop_boost()  # Appeler la méthode pour arrêter le boost
        return redirect(reverse('boosted_post_list'))

class DeleteBoostView(LoginRequiredMixin,View):
    def post(self, request, pk):
        boosted_post = get_object_or_404(BoostedPost, pk=pk)
        boosted_post.delete_boost()  # Appeler la méthode pour supprimer le boost
        boosted_post.delete()
        return redirect(reverse('boosted_post_list'))
# function boost pub fin






def reply_to_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        reply_message = request.POST.get('reply_message')

        # Ici, vous pouvez utiliser votre fonction pour envoyer la réponse via l'API Facebook
        reply_to_comment(comment_id, reply_message, ACCESS_TOKEN)

        return redirect('your_template_name')


# Fonction existante pour récupérer les données depuis Facebook
from django.utils import timezone


def get_facebook_post_info_from_db(access_token):
    # Récupérer toutes les publications sauvegardées dans la base de données
    posts = PostPublication.objects.all()
    print(f"Nombre de publications trouvées : {posts.count()}")  # Débogage

    if not posts.exists():
        print("Aucune publication trouvée dans la base de données.")
        return

    for post in posts:
        post_id = post.id_publication  # Assurez-vous que ce champ contient l'ID de publication Facebook
        print(f"Publication ID dans la base de données : {post_id}")  # Débogage

        if not post_id:
            print(f"Aucun ID de publication pour la publication avec l'ID {post.id}.")
            continue

        print(f"Tentative de récupération des informations pour la publication ID: {post_id}")

        # URL pour récupérer les informations de la publication
        url = f"https://graph.facebook.com/v16.0/{post_id}"
        params = {
            'fields': 'created_time,from,message,likes.summary(true),comments.summary(true){id,message,from,created_time}',
            'access_token': access_token
        }

        # Faire la requête
        response = requests.get(url, params=params)
        print(f"Réponse brute de l'API : {response.text}")  # Débogage

        if response.status_code == 200:
            data = response.json()

            # Vérification de l'existence de 'from'
            from_info = data.get('from', {})
            posted_by = from_info.get('name', 'Inconnu') if from_info else 'Inconnu'

            likes_summary = data.get('likes', {}).get('summary', {})
            comments_summary = data.get('comments', {}).get('summary', {})
            comments = data.get('comments', {}).get('data', [])

            # Mettre à jour les informations de la publication
            post.message = data.get('message', post.message)  # Assurez-vous que ceci est un champ valide
            post.created_at = data.get('created_time', post.created_at)  # Vérifiez que created_at est défini
            post.save()  # Sauvegarder les modifications de la publication

            # Enregistrer les likes
            if likes_summary:
                likes_count = likes_summary.get('total_count', 0)
                print(f"Nombre de likes : {likes_count}")

                # Récupérer les likes (cette partie peut nécessiter une autre requête si vous voulez les détails des likes)
                for _ in range(likes_count):  # Simulation de l'ajout des likes
                    # Exemple de logique pour ajouter les likes
                    Like.objects.get_or_create(
                        post_type=post,
                        liker_id='example_liker_id',  # Remplacez par l'ID de l'utilisateur qui a liké
                        liker_name='Example Liker'  # Remplacez par le nom de l'utilisateur qui a liké
                    )

            # Enregistrer les commentaires
            if comments:
                for comment in comments:
                    comment_id = comment['id']  # Récupérer l'ID du commentaire
                    commenter_name = comment['from'].get('name', 'Inconnu') if 'from' in comment else 'Inconnu'
                    comment_message = comment.get('message', 'Aucun message')
                    created_time = comment.get('created_time', timezone.now())

                    # Créer ou mettre à jour chaque commentaire
                    Comment.objects.update_or_create(
                        comment_id=comment_id,
                        defaults={
                            'post': post,  # Associé à la publication
                            'message': comment_message,
                            'commenter_name': commenter_name,
                            'created_time': created_time,
                        }
                    )

            print(f"Informations enregistrées pour la publication ID: {post_id}")
        else:
            error_data = response.json().get('error', {})
            error_message = error_data.get('message', 'Erreur inconnue')
            error_code = error_data.get('code', 'Aucun code')
            print(f"Erreur {response.status_code} pour la publication {post_id}: {error_message} (Code: {error_code})")

def afficher_publications(request):
    # Token d'accès à l'API Facebook (doit être sécurisé)
    access_token = "EAAHZAsb1umoIBOwiDlKriZAXVNBeIGiEmLGrD1DputhuvZBNGTBepaLToxBAVrfSznxskwC06Vjb08ELmwLKyZAEkLFTU3Hyhqrneety6bCL64C69j2y1FiEqbeJNlDpit3vWMA0imz1tnWkM3VmtBPcNUXd65ZCox1f6VezZBFWr0jKeWZCe5Kh75ZA44MReoTBpDbXU2ZC4USHZC5VZComryWxoXN"

    # Récupérer et sauvegarder les informations des publications dans la base de données
    posts_info = get_facebook_post_info_from_db(access_token)

    # Passer les informations au template
    return render(request, 'services/afficher_publications.html', {
        'posts_info': posts_info
    })










@csrf_exempt
def like_publication(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')  # Récupérer l'ID de l'utilisateur (si disponible)
        access_token = "EAAHZAsb1umoIBOwiDlKriZAXVNBeIGiEmLGrD1DputhuvZBNGTBepaLToxBAVrfSznxskwC06Vjb08ELmwLKyZAEkLFTU3Hyhqrneety6bCL64C69j2y1FiEqbeJNlDpit3vWMA0imz1tnWkM3VmtBPcNUXd65ZCox1f6VezZBFWr0jKeWZCe5Kh75ZA44MReoTBpDbXU2ZC4USHZC5VZComryWxoXN"

        # Envoyer la requête à l'API Facebook pour liker la publication
        url = f"https://graph.facebook.com/v16.0/{post_id}/likes"
        params = {'access_token': access_token}
        response = requests.post(url, params=params)

        if response.status_code == 200:
            # Enregistrer le like dans la base de données
            like = Like(post_id=post_id, user_id=user_id)
            like.save()

            # Récupérer le nombre actuel de likes
            likes_url = f"https://graph.facebook.com/v16.0/{post_id}?fields=likes.summary(true)"
            likes_response = requests.get(likes_url, params=params)
            if likes_response.status_code == 200:
                new_likes_count = likes_response.json().get('likes', {}).get('summary', {}).get('total_count', 0)
                return JsonResponse({'new_likes_count': new_likes_count})
            else:
                return JsonResponse({'error': 'Impossible de récupérer le nouveau nombre de likes'}, status=500)
        else:
            return JsonResponse({'error': 'Échec du like'}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)







# def get_publications(request):
#     publications = PostPublication.objects.prefetch_related('comments', 'likes').all()
#     data = []
#
#     for publication in publications:
#         data.append({
#             'id_publication': publication.id_publication,
#             'post_type': publication.post_type,
#             'message': publication.message,
#             'description': publication.description,
#             'created_at': publication.created_at,
#             'comments_count': publication.comments.count(),
#             'comments_ids': [comment.comment_id for comment in publication.comments.all()],
#             'likes_count': publication.likes.count()
#         })
#
#     return JsonResponse(data, safe=False)


# class SaveFacebookPostView(View):
#     def get(self, request, *args, **kwargs):
#         access_token = "EAAHZAsb1umoIBOZB76FM28YLQBchTu8YacXlo9ZCJRRIJULIO7FenyIVwHPc0VmT6ibFwMZBHksH9pZCKV7dxrUqBVnmCxobZCU7SKPGhZBKXkshYnVGCErOR4MkgfOuzvAfZC7By8whzdVszOlMfu96s7PByOc1IOasH0nTuyK4RwuZByNa7cSEjHCzXv8DKGlLMUdDDFQWoTZBZBhlgR513IshMiA"  # Remplacez par votre token
#
#         # Récupérer toutes les publications de la base de données
#         posts = PostPublication.objects.all()
#
#         if not posts.exists():
#             return JsonResponse({"error": "Aucune publication trouvée dans la base de données."}, status=404)
#
#         for post in posts:
#             post_id = post.id_publication
#
#             # URL pour récupérer les informations de la publication
#             url = f"https://graph.facebook.com/v16.0/{post_id}"
#             params = {
#                 'fields': 'created_time,from,message,likes.summary(true),comments.summary(true){id,message,from,created_time}',
#                 'access_token': access_token
#             }
#
#             # Faire la requête
#             response = requests.get(url, params=params)
#
#             if response.status_code == 200:
#                 data = response.json()
#
#                 # Sauvegarde des informations de la publication
#                 post.message = data.get('message', post.message)
#                 post.created_at = data.get('created_time', post.created_at)
#                 post.save()
#
#                 # Sauvegarde des commentaires
#                 comments = data.get('comments', {}).get('data', [])
#                 for comment in comments:
#                     comment_id = comment['id']
#                     commenter_name = comment['from']['name']
#                     message = comment['message']
#                     created_time = comment['created_time']
#
#                     # Enregistrer ou mettre à jour chaque commentaire
#                     Comment.objects.update_or_create(
#                         comment_id=comment_id,
#                         defaults={
#                             'post': post,
#                             'comment_id': comment_id,
#                             'message': message,
#                             'commenter_name': commenter_name,
#                             'created_time': created_time,
#                         }
#                     )
#             else:
#                 return JsonResponse({"error": f"Erreur lors de la récupération de la publication {post_id}"}, status=response.status_code)
#
#         return JsonResponse({"success": "Les informations ont été mises à jour avec succès."}, status=200)