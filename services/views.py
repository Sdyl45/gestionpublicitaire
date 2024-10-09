from cloudinary.utils import cloudinary_url
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.backends import django
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from facebook_business.adobjects.page import Page
import cloudinary.uploader
from core.api.createCampaign import create_campaign
from core.api.createPublicite import create_ad_set
from .forms import CampaignForm, AudienceForm,LocationForm,PubliciteForm,EditPudForm,EditCampagneForm,PostPublicationForm,BoostedPostForm,EditPostPublicationForm
from .models import Campaign, Audience, Location, Publicite, PostPublication, BoostedPost, Comment, Like
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

import logging
logger = logging.getLogger(__name__)
class modifierCampagneView(LoginRequiredMixin, UpdateView):
    template_name = 'services/MesCampagme.html'
    model = Campaign
    form_class = EditCampagneForm
    success_url = reverse_lazy('CampagneList')

    def form_valid(self, form):
        try:
            # Récupérer l'instance actuelle de la campagne
            instance = form.save(commit=False)

            # Tenter de mettre à jour la campagne sur Facebook
            facebook_id = instance.facebookCampaign_ID

            # Appel à la fonction de mise à jour de la campagne
            success = update_facebook_campaign(
                facebook_id,
                name=form.cleaned_data.get('name'),
                objective=form.cleaned_data.get('objective'),
                budget=form.cleaned_data.get('budget'),
                status=form.cleaned_data.get('status')
            )

            if not success:
                form.add_error(None, "La mise à jour de la campagne sur Facebook a échoué.")
                return self.form_invalid(form)

            # Sauvegarder les modifications locales si la mise à jour sur Facebook est réussie
            instance.save()

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, f"Une erreur s'est produite : {str(e)}")
            return self.form_invalid(form)


# Fonction de mise à jour de la campagne sur Facebook
def update_facebook_campaign(campaign_id, name, objective, budget, status):
    """
    Met à jour une campagne Facebook avec les informations fournies.
    """
    update_url = f"https://graph.facebook.com/v17.0/{campaign_id}"
    params = {
        'access_token': '<YOUR_ACCESS_TOKEN>',  # Remplacez par votre jeton d'accès
        'name': name,
        'objective': objective,
        'daily_budget': budget,  # Assurez-vous que ce soit bien au format requis par l'API
        'status': status
    }

    # Envoyer la requête de mise à jour à l'API Facebook
    try:
        response = requests.post(update_url, params=params)
        response.raise_for_status()  # Vérifier s'il y a une erreur
        return True
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la mise à jour de la campagne Facebook: {e}")
        return False


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







# Configuration de Cloudinary
cloudinary.config(
    cloud_name="dtylzz2iu",
    api_key="639229414146889",
    api_secret="tbG6cUvsqR5Trt9fBT_wpTxATHo",
    secure=True
)

class ListPostsView(LoginRequiredMixin, TemplateView):
    """
    Vue Django pour lister et enregistrer les publications d'une page Facebook dans un DataTable
    et enregistrer les informations des likes et commentaires en base de données.
    """
    template_name = 'services/liste_posts.html'
    page_id = '434662436390612'  # ID de la page Facebook
    access_token = 'EAAHZAsb1umoIBOwNA6CucCMd1SBJqZARrUgzz7HTCkdd4ZAdxqISzEuQrfLINrwA0gD9EtCZAodU1X2I5MfSpkHDTVO0ZCrQ8VCL2vn1ZAVJ1CKOJxXsIgjXJr22kZC3P6JyO7zZBc5SloOBLgDQ877GCwYePx10a1fEZANmX2Q3NCr09uZBwdr8Je2GeQAPq7TneikReXApvrWwGOsgsOyhp8Fyxz'  # Jeton d'accès Facebook

    def get_context_data(self, **kwargs):
        """
        Ajoute les publications Facebook, les likes et les commentaires au contexte pour affichage dans le template.
        """
        context = super().get_context_data(**kwargs)

        # Appel API pour récupérer les publications Facebook
        posts = self.get_posts()

        # Ajouter les publications, likes et commentaires au contexte
        context['posts'] = posts
        return context

    def get_posts(self):
        """
        Récupère les publications de la page Facebook via l'API, les enregistre en base de données,
        et renvoie une liste de publications avec leurs likes et commentaires.
        """
        get_posts_url = f'https://graph.facebook.com/v17.0/{self.page_id}/posts'
        get_posts_params = {
            'access_token': self.access_token
        }

        response = requests.get(get_posts_url, params=get_posts_params)

        if response.status_code == 200:
            info_post = response.json()
            posts = info_post.get('data', [])

            # Récupérer les IDs des publications déjà présentes en base de données
            existing_ids = set(PostPublication.objects.values_list('id_publication', flat=True))

            for post in posts:
                post_id = post.get('id')
                if post_id in existing_ids:
                    continue  # Passer les publications déjà présentes

                # Créer ou obtenir une instance de PostPublication
                post_obj, created = PostPublication.objects.get_or_create(
                    id_publication=post_id,
                    defaults={
                        'post_type': post.get('type', ''),
                        'message': post.get('message', ''),
                        'description': post.get('story', ''),
                        'created_at': post.get('created_time'),
                        'user': self.request.user
                    }
                )

                # Récupérer les likes et les commentaires
                self._fetch_likes(post_obj)
                self._fetch_comments(post_obj)

            return posts
        else:
            print(f"Erreur lors de la récupération des publications: {response.status_code}")
            return []

    def _fetch_likes(self, post_obj):
        """
        Récupère les likes associés à une publication Facebook et les enregistre.
        """
        likes_url = f"https://graph.facebook.com/v17.0/{post_obj.id_publication}/likes"
        params = {'access_token': self.access_token}
        response = requests.get(likes_url, params=params)

        if response.status_code == 200:
            likes_data = response.json().get('data', [])
            for like in likes_data:
                liker_id = like.get('id')
                liker_name = like.get('name', 'Inconnu')

                # Enregistrer le like dans la base de données
                Like.objects.update_or_create(
                    liker_id=liker_id,
                    post=post_obj,
                    defaults={'liker_name': liker_name}
                )
        else:
            print(f"Erreur lors de la récupération des likes : {response.text}")

    def _fetch_comments(self, post_obj):
        """
        Récupère les commentaires associés à une publication Facebook et les enregistre.
        """
        comments_url = f"https://graph.facebook.com/v17.0/{post_obj.id_publication}/comments"
        params = {'access_token': self.access_token}
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
                    post=post_obj,
                    defaults={
                        'message': message,
                        'commenter_name': commenter_name,
                        'created_time': created_time,
                    }
                )
        else:
            print(f"Erreur lors de la récupération des commentaires : {response.text}")








class PublishContentView(LoginRequiredMixin, CreateView):
    model = PostPublication
    template_name = 'services/CreerPublication.html'
    form_class = PostPublicationForm
    success_url = reverse_lazy('liste_posts')

    page_id = '434662436390612'
    access_token = 'EAAHZAsb1umoIBOwNA6CucCMd1SBJqZARrUgzz7HTCkdd4ZAdxqISzEuQrfLINrwA0gD9EtCZAodU1X2I5MfSpkHDTVO0ZCrQ8VCL2vn1ZAVJ1CKOJxXsIgjXJr22kZC3P6JyO7zZBc5SloOBLgDQ877GCwYePx10a1fEZANmX2Q3NCr09uZBwdr8Je2GeQAPq7TneikReXApvrWwGOsgsOyhp8Fyxz'
    media_directory = r'C:\Users\LYAN\PycharmProjects\GestionPublicitaire\static\images'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user

        # Préparer les URLs des médias pour publication
        media_urls = self._upload_media_to_cloudinary(post)

        # Publier le contenu sur Facebook
        if 'video_url' in media_urls:
            response = self._publish_video_to_facebook(post, media_urls)
        else:
            response = self._publish_to_facebook(post, media_urls)

        if 'error' in response:
            form.add_error(None, f"Erreur lors de la publication sur Facebook: {response['error']}")
            return self.form_invalid(form)

        post.id_publication = response.get('id')
        post.save()

        return super().form_valid(form)

    def _upload_media_to_cloudinary(self, post):
        """
        Upload les images et vidéos sur Cloudinary et retourne les URLs optimisées.
        """
        media_urls = {}

        # Upload image si disponible
        if post.image:
            image_path = os.path.join(self.media_directory, post.image.name)
            upload_result = cloudinary.uploader.upload(image_path)
            media_urls['image_url'] = upload_result['secure_url']  # URL sécurisée de l'image

        # Upload vidéo si disponible
        if post.video:
            video_path = os.path.join(self.media_directory, post.video.name)
            upload_result = cloudinary.uploader.upload_large(video_path, resource_type="video")
            media_urls['video_url'] = upload_result['secure_url']  # URL sécurisée de la vidéo

        return media_urls

    def _publish_to_facebook(self, post, media_urls):
        """
        Publie un message avec une image sur Facebook.
        """
        url = f"https://graph.facebook.com/v17.0/{self.page_id}/feed"

        params = {
            'message': post.message,
            'access_token': self.access_token,
        }

        # Ajouter l'URL de l'image si elle existe
        if 'image_url' in media_urls:
            params['image'] = media_urls['image_url']  # Ajoute l'image de Cloudinary

        # Publier la requête
        response = requests.post(url, data=params)
        return response.json()

    def _publish_video_to_facebook(self, post, media_urls):
        """
        Publie une vidéo sur Facebook via l'API vidéo.
        """
        url = f"https://graph.facebook.com/v17.0/{self.page_id}/videos"
        params = {
            'description': post.message,  # Utilise le message comme description de la vidéo
            'access_token': self.access_token,
        }

        # Ajouter l'URL de la vidéo si elle existe
        if 'video_url' in media_urls:
            params['file_url'] = media_urls['video_url']  # Ajoute la vidéo de Cloudinary

        # Publier la vidéo
        response = requests.post(url, data=params)
        return response.json()






class EditPostView(LoginRequiredMixin, UpdateView):
    model = PostPublication
    template_name = 'services/CreatePublication.html'
    form_class = EditPostPublicationForm
    success_url = reverse_lazy('liste_posts')

    def get_object(self, queryset=None):
        # Utiliser get_object_or_404 pour obtenir la publication
        return get_object_or_404(PostPublication, id_publication=self.kwargs['pk'])

    def form_valid(self, form):
        # Récupérer l'objet de la publication modifiée
        post_obj = form.save(commit=False)

        # Initialiser l'API Facebook avec le ACCESS_TOKEN
        access_token = 'EAAHZAsb1umoIBOZBO9Ng0uugJZCZAEiITAeizYgGRofUEfZCWztBTepZAlIIATL902DKAotIf1IbdZAZC1yZBLZChzagjobnvAEJZACvXa76a3tLq2DLkwjsTPGJTUhotxDPOkpNRZBkrJ6EWZCJTEgrt7CX3SUQF5ZBdZCpOHxVl8cdd47hcZB7EMTGRtR17ZAb3lPH7WZCZCDWhgFcfN8DC2bEI6DlKlPgz5ZC'  # Remplacer par votre propre access_token
        page_id = '434662436390612'  # Remplacer par l'ID de votre page Facebook
        FacebookAdsApi.init(access_token=access_token)

        # Obtenir l'ID de la publication Facebook
        fb_post_id = post_obj.id_publication

        try:
            # Modifier la publication sur Facebook via l'API
            page = Page(page_id)
            post_params = {
                'message': post_obj.message,
                # Ajoutez d'autres champs que vous voulez modifier, comme la vidéo ou l'image
            }
            page_post = page.update_post(fb_post_id, params=post_params)

            # Sauvegarder la modification dans la base de données
            post_obj.save()

            messages.success(self.request,
                             "La publication a été modifiée avec succès, à la fois dans l'API Facebook et dans la base de données.")
        except Exception as e:
            # Gérer les erreurs possibles lors de l'appel à l'API Facebook
            messages.error(self.request,
                           f"Une erreur s'est produite lors de la modification de la publication sur Facebook : {e}")
            return self.form_invalid(form)

        return HttpResponseRedirect(self.success_url)






class detailPublicationView(LoginRequiredMixin,DetailView):
    template_name = 'services/DetailPublication.html'
    model = PostPublication
    context_object_name = 'publication'

class DeletePostView(LoginRequiredMixin,DeleteView):
    model = PostPublication
    template_name = 'services/confirm_delete.html'
    success_url = reverse_lazy('liste_posts')



@csrf_exempt  # Assurez-vous d'utiliser csrf_exempt uniquement si nécessaire
def send_reply_to_api(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        message = request.POST.get('message')

        # Logique pour envoyer la réponse à l'API
        try:
            # Remplacez par l'URL de votre API
            api_url = 'https://api.example.com/reply'
            payload = {
                'comment_id': comment_id,
                'message': message
            }
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                # Enregistrer la réponse dans la base de données
                Comment.objects.create(
                    comment_id=comment_id,  # Utilisez un identifiant approprié
                    message=message,
                    commenter_name=request.user.username,  # Ou l'adapter selon vos besoins
                    created_time=timezone.now(),
                    post_id=...  # Assurez-vous de lier cela à la publication
                )
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Erreur de l\'API.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})


def check_publication_status(request):
    # Récupérer toutes les publications
    publications = PostPublication.objects.all()

    # Créer une liste de publications avec les données nécessaires
    posts_data = []
    for post in publications:
        posts_data.append({
            'id': post.id,
            'id_publication': post.id_publication,
            'message': post.message,
            'created_at': post.created_at.isoformat(),
            'comment_count': post.comment_count,
            'like_count': post.like_count,
        })

    # Retourner les données sous forme de JSON
    return JsonResponse({'posts': posts_data})
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
        access_token = "EAAHZAsb1umoIBO4wmn4B9nKtOLHeCK6HKbDhh2YR7OoTqKZAZBZBZCe4K2B1MsLZArBbSZAFGcYa0UhjnxezcJhQZCz38Ct2FLZC08GqePYQRbQDIGoUXMOKsJdBRHQ38Skgsa4DAckc0HEFmsbUoKi4hKMVGe2KEn2wJX3LZBQNmeqqocX0bxGyGNgukEbLQGL0AwF19z2wPzUcyuGzO1vOPBlrfV"

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



