from django.shortcuts import render,redirect
from django.http import HttpResponse

from core.api.createCampaign import create_campaign
from core.api.createPublicite import create_ad_set
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



class CreatePubliciteView(LoginRequiredMixin, CreateView):
    template_name = 'services/CreerPublication.html'
    model = Publicite
    form_class = PubliciteForm
    success_url = reverse_lazy('listPubs')

    def form_valid(self, form):
        campagne_id = self.kwargs.get('pk')

        try:
            campagne = Campaign.objects.get(pk=campagne_id)
        except Campaign.DoesNotExist:
            form.add_error(None, "La campagne demandée n'existe pas.")
            return self.form_invalid(form)

        ad_set_id = create_ad_set(int(campagne.facebookCampaign_ID), form.cleaned_data.get('name'))


        if ad_set_id is None:
            form.add_error(None, "Échec de la création de l'ensemble de publicités.")
            return self.form_invalid(form)

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


class ListPostsView(LoginRequiredMixin, TemplateView):
    """
    Vue Django pour lister les publications d'une page Facebook dans un DataTable.
    """
    template_name = 'services/liste_posts.html'
    page_id = '434662436390612'  # ID de la page Facebook
    access_token = 'EAAHZAsb1umoIBO8FLH4QB9w3h1FZCQFRVPe6ap2Li0O8F989LXn3KIRr17zDYK2oBrMdjAWPHpMZBMIVK0QuPJNa4bgcJAiH01cWmZAebNbulipDQr7wPWHkg3TxFgPqEjRzNMAW1JLVR34yP3wYRQc7NfiG9XBNpz56AZCpCmRDNWgoSgOdUfpWCPdqDbx61NRief3GvlgwRHxy1iZBZBIlYS4ltr00X85'  # Jeton d'accès Facebook

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Appel API pour récupérer les publications
        posts = self.get_posts()

        print(posts)  # Vérifie les données dans la console

        # Ajouter les posts récupérés au contexte
        context['posts'] = posts
        return context

    def get_posts(self):
        """
        Récupère les publications de la page Facebook et renvoie une liste de posts.
        """
        get_posts_url = f'https://graph.facebook.com/v17.0/{self.page_id}/posts'
        get_posts_params = {
            'access_token': self.access_token
        }

        response = requests.get(get_posts_url, params=get_posts_params)

        if response.status_code == 200:
            info_post = response.json()
            return info_post.get('data', [])  # Retourne la liste des publications
        else:
            print(f"Erreur lors de la récupération des publications: {response.status_code} - {response.json()}")
            return []







class PublishContentView(LoginRequiredMixin, CreateView):
    model = PostPublication
    template_name = 'services/CreerPublication.html'
    form_class = PostPublicationForm
    success_url = reverse_lazy('liste_posts')

    # ID de la page Facebook et jeton d'accès
    page_id = '434662436390612'
    access_token = 'EAAHZAsb1umoIBO3XMFPOdJYjx00pS2xsXaHtqcylfZC2MZCRXM6VZCIGl46gcMQud0wMZCm9UL1p7dtnpuacbdQQG66L9iyoHuDl0icSXxjuwacq6h6qmZC1kC37hZAyeqMaYsjwCwxBaZCLesEUmD9IRnZCPAbsuH2gUHHeONuppKyTrXBUaWoJNBM8PADtpmH1qIWmmU029OxVCAiKNqJRvuuxLdaphci9I'

    # Chemin vers le répertoire des images et vidéos
    media_directory = r'C:\Users\LYAN\PycharmProjects\GestionPublicitaire\static\images'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user

        response = self._publish_to_facebook(post)

        if 'error' in response:
            form.add_error(None, f"Erreur lors de la publication sur Facebook: {response['error']}")
            return self.form_invalid(form)

        post.id_publication = response.get('id')
        post.save()

        return super().form_valid(form)

    def _publish_to_facebook(self, post):
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
        post_url = f'https://graph.facebook.com/v17.0/{self.page_id}/feed'
        post_params = {
            'message': message,
            'access_token': self.access_token
        }
        response = requests.post(post_url, data=post_params)
        return self._handle_response(response)

    def _publish_image(self, image_path, message):
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







def accCondition(request):
    return render(request, 'services/acceuilConditionsConf.html')

def accConditionConf(request):
    """
    Vue pour la page des conditions de confidentialité.
    """
    return render(request, 'services/Aconfidentialite.html')