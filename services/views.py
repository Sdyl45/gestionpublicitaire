from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CampaignForm, AudienceForm,LocationForm,PubliciteForm,EditPudForm,EditCampagneForm,PostPublicationForm
from .models import Campaign, Audience,Location,Publicite,PostPublication
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from services import FacebookService
import os
import requests
from django.views.generic import TemplateView
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


class liste_campagnesView(ListView):
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


ACCESS_TOKEN = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
ACCOUNT_ID = 'act_1822221194968260'

# Initialiser l'API
FacebookAdsApi.init(access_token=ACCESS_TOKEN)
class CreerCampagneView(LoginRequiredMixin, CreateView):
    template_name = 'services/MesCampagme.html'
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy('CampagneList')

    def form_valid(self, form):
        # Sauvegarder la campagne
        self.object = form.save()

        # Appeler la fonction pour créer la campagne dans Facebook
        try:
            # Créer une instance de AdAccount
            account = AdAccount(ACCOUNT_ID)

            # Définir les paramètres de la campagne
            params = {
                'name': self.object.name,  # Utiliser le nom de la campagne sauvegardée
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'PAUSED',
                'special_ad_categories': [],
            }

            # Créer la campagne
            campaign = account.create_campaign(fields=[], params=params)
            print(f"Campaign created with ID: {campaign['id']}")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la création de la campagne : {e}")
            # Vous pourriez vouloir gérer l'erreur, par exemple en affichant un message d'erreur

        # Vérifier si l'utilisateur souhaite créer une publicité
        if form.cleaned_data.get('create_ad'):
            return redirect('publication')  # Remplacez par le nom de votre URL pour créer une publicité

        return super().form_valid(form)

class modifierCampagneView(UpdateView):
    template_name = 'services/MesCampagme.html'
    model = Campaign
    form_class = EditCampagneForm
    success_url = reverse_lazy('CampagneList')


class deletecampagneView(DeleteView):
    template_name = 'services/dropPub.html'
    model = Campaign
    context_object_name = 'campagne'
    success_url = reverse_lazy('CampagneList')
def RapportsCampViews(request):
 return render(request,'services/CreerRapportsCampagne.html')



class detailcampagneView(DetailView):
    template_name = 'services/DetailCampagne.html'
    model = CampaignForm
    context_object_name = 'campagne'
# creation de campagnes views fin

# creation de publicite views debut


#
# def creer_publicite(request):
#     if request.method == 'POST':
#         form = PubliciteForm(request.POST, request.FILES)  # N'oubliez pas de gérer les fichiers
#         if form.is_valid():
#             form.save()  # Enregistrer la publicité dans la base de données
#             return redirect('listPubs')  # Redirigez vers une page de liste ou une autre page
#     else:
#         form = PubliciteForm()
#
#     return render(request, 'services/CreerPublication.html', {'form': form})

# class CreatePubliciteViews(LoginRequiredMixin,UserPassesTestMixin, CreateView):

# Remplacez par vos informations
ACCESS_TOKEN = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
ACCOUNT_ID = 'act_1822221194968260'
APP_ID = '520832387291778'

# Initialiser l'API Facebook
FacebookAdsApi.init(access_token=ACCESS_TOKEN)

class CreatePubliciteView(LoginRequiredMixin, CreateView):
    template_name = 'services/CreerPublication.html'
    model = Publicite
    form_class = PubliciteForm
    success_url = reverse_lazy('listPubs')

    def form_valid(self, form):
        self.object = form.save()  # Sauvegarder la publicité

        # Récupérer les champs supplémentaires du formulaire
        campagne = self.object.campaign
        statut = self.object.statut
        budget_quotidien = self.object.budget_quotidien
        objectif_optimisation = self.object.objectif_optimisation
        evenement_facturation = self.object.evenement_facturation

        try:
            # Vérifier l'état de la campagne
            campaign = Campaign(campagne.campaign_id)
            campaign_data = campaign.api_get(fields=['id', 'name', 'status'])

            if campaign_data['status'] == 'ARCHIVED':
                print("La campagne est archivée. Veuillez l'activer avant de créer des ensembles de publicités.")
                return super().form_invalid(form)  # Échouer le formulaire si la campagne est archivée

            # Paramètres de l'ensemble de publicités
            params = {
                'name': self.object.name,
                'optimization_goal': objectif_optimisation,
                'billing_event': evenement_facturation,
                'bid_amount': '250',  # Exemple de montant d'enchère
                'daily_budget': str(int(budget_quotidien) * 100),  # En centimes
                'campaign_id': campagne.campaign_id,  # Utiliser l'ID de la campagne sélectionnée
                'status': statut,
                'promoted_object': {
                    'application_id': APP_ID,
                    'custom_event_type': 'PURCHASE'
                },
                'targeting': {
                    'geo_locations': {
                        'countries': ['FR'],  # Exemple de ciblage géographique
                    },
                    'age_min': 18,
                    'age_max': 65,
                    'genders': [1],  # 1 pour femme, 2 pour homme
                },
            }

            # Créer l'objet AdAccount
            ad_account = AdAccount(ACCOUNT_ID)

            # Créer l'ensemble de publicités sur Facebook
            ad_set = ad_account.create_ad_set(params=params)
            print(f"Ensemble de publicités créé avec succès : {ad_set}")

        except Exception as e:
            print(f"Une erreur s'est produite lors de la création de l'ensemble de publicités : {e}")
            return super().form_invalid(form)  # Échouer le formulaire en cas d'erreur

        return super().form_valid(form)


class modifierPubliciteView(UpdateView):
    template_name = 'services/CreerPublication.html'
    model = Publicite
    form_class = EditPudForm
    success_url = reverse_lazy('listPubs')


class deletepubliciteView(DeleteView):
    template_name = 'services/dropPub.html'
    model = Publicite
    context_object_name = 'publicite'
    success_url = reverse_lazy('listPubs')


class detailPubliciteView(DetailView):
    template_name = 'services/DetailPublicite.html'
    model = Publicite
    context_object_name = 'publicite'
def list_pubs(request):
    publicites = Publicite.objects.all()  # Récupère toutes les publicités
    return render(request, 'services/ListPubs.html', {'publicites': publicites})


def CreatePublicationView(request):
 return render(request,'services/createPublication.html')
# creation de publicite views fin


class CreateAudienceView(CreateView):
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
class UpdateAudienceView(UpdateView):
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
class AudienceListView(ListView):
    model = Audience
    template_name = 'services/Audience_list.html'
    context_object_name = 'audiences'

    def get_queryset(self):
        return Location.objects.all()


# Vue pour supprimer une audience
class DeleteAudienceView(DeleteView):
    model = Audience
    template_name = 'services/DeleteAudience.html'
    success_url = reverse_lazy('audience_list')


# create audience fin

# create localisation debut
class CreateLocationView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'services/CreerLocation.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        form.instance.audience_id = self.kwargs['audience_id']  # Associe la localisation à une audience
        return super().form_valid(form)


# Vue pour mettre à jour une localisation existante
class UpdateLocationView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'services/CreerLocation.html'
    success_url = reverse_lazy('location_list')


# Vue pour afficher la liste des localisations
class LocationListView(ListView):
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


class PostsListView(LoginRequiredMixin, TemplateView):
    template_name = 'services/liste_posts.html'

    # ID de la page Facebook et token d'accès
    page_id = '434662436390612'
    access_token = 'EAAHZAsb1umoIBOxZCZBmogImHZBR5zAv6rodKAaRFCaeYB7yDFpxGV2eJLaWpe9ZBsNA5PEhyZBwZCjyLzZARDWohd0ZC2kWgzDPo08ypZCXZCQZBEYFTjGFcFocBBh21tZAm9lQmwiefmejPC7eoylO7SETmJKrRkL4HRVCnUPChyodE48Ahy4NT6QlZBlH0ZBgzoMxfeVNARbbZBvjsR9ac80RsSpfZCTDb3bbHhxk3'

    def get_posts(self):
        """
        Récupère les publications de la page Facebook via l'API Graph.
        """
        url = f'https://graph.facebook.com/v17.0/{self.page_id}/posts'
        params = {
            'access_token': self.access_token
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            return []

    def get_context_data(self, **kwargs):
        """
        Ajoute les données des posts au contexte.
        """
        context = super().get_context_data(**kwargs)
        posts = self.get_posts()  # Récupère les posts de l'API
        context['posts'] = posts  # Ajoute les posts au contexte pour le template
        return context






class PublishContentView(LoginRequiredMixin, CreateView):
    """
    Vue Django pour créer et publier du contenu sur un profil Facebook.
    """
    model = PostPublication
    template_name = 'services/CreerPublication.html'
    form_class = PostPublicationForm
    success_url = reverse_lazy('liste_posts')

    def form_valid(self, form):
        # Préparer l'objet mais ne pas le sauvegarder immédiatement
        post = form.save(commit=False)
        post.user = self.request.user  # Associe l'utilisateur connecté

        # Informations de l'utilisateur Facebook et jeton d'accès
        profile_id = '434662436390612'  # ID du profil utilisateur Facebook
        access_token = 'EAAHZAsb1umoIBO8FLH4QB9w3h1FZCQFRVPe6ap2Li0O8F989LXn3KIRr17zDYK2oBrMdjAWPHpMZBMIVK0QuPJNa4bgcJAiH01cWmZAebNbulipDQr7wPWHkg3TxFgPqEjRzNMAW1JLVR34yP3wYRQc7NfiG9XBNpz56AZCpCmRDNWgoSgOdUfpWCPdqDbx61NRief3GvlgwRHxy1iZBZBIlYS4ltr00X85'
        base_url = f'https://graph.facebook.com/{profile_id}'

        # Publication en fonction du type de post
        response = self._publish_to_facebook(post, base_url, access_token)

        # Gestion des erreurs de publication
        if 'error' in response:
            form.add_error(None, f"Erreur lors de la publication sur Facebook: {response['error']}")
            return self.form_invalid(form)

        # Si la publication sur Facebook réussit, on sauvegarde l'ID de publication
        post.id_publication = response.get('id')

        # Sauvegarde de l'objet PostPublication dans la base de données
        post.save()

        return super().form_valid(form)

    def _publish_to_facebook(self, post, base_url, access_token):
        """
        Publie le contenu sur Facebook en fonction du type de publication (message, image, vidéo).
        """
        if post.post_type == 'message':
            return self._publish_message(post.message, base_url, access_token)
        elif post.post_type == 'image' and post.image:
            return self._publish_image(post.message, post.image, base_url, access_token)
        elif post.post_type == 'video' and post.video:
            return self._publish_video(post.description, post.video, base_url, access_token)
        else:
            return {"error": "Type de publication non pris en charge."}

    def _publish_message(self, message, base_url, access_token):
        """
        Publie un message texte sur le profil Facebook.
        """
        url = f'{base_url}/feed'
        params = {
            'message': message,
            'access_token': access_token
        }
        return self._make_request(url, params)

    def _publish_image(self, message, image_file, base_url, access_token):
        """
        Publie une image accompagnée d'un message sur le profil Facebook.
        """
        url = f'{base_url}/photos'
        files = {'source': image_file}
        data = {
            'message': message,
            'access_token': access_token
        }
        return self._make_request(url, data, files)

    def _publish_video(self, description, video_file, base_url, access_token):
        """
        Publie une vidéo accompagnée d'une description sur le profil Facebook.
        """
        url = f'{base_url}/videos'
        files = {'source': video_file}
        data = {
            'description': description,
            'access_token': access_token
        }
        return self._make_request(url, data, files)

    def _make_request(self, url, data, files=None):
        """
        Effectue une requête HTTP vers l'API Facebook.
        """
        response = requests.post(url, data=data, files=files) if files else requests.post(url, data=data)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Gère la réponse de l'API Facebook et renvoie le résultat ou une erreur.
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

    def form_invalid(self, form):
        """
        Gère la réponse dans le cas où le formulaire est invalide.
        """
        return super().form_invalid(form)



def accCondition(request):
    return render(request, 'services/acceuilConditionsConf.html')

def accConditionConf(request):
    """
    Vue pour la page des conditions de confidentialité.
    """
    return render(request, 'services/Aconfidentialite.html')