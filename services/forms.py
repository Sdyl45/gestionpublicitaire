from django import forms
from django.forms import ModelForm

from .models import Campaign,Audience, Location,Publicite
from django import forms
from .models import PostPublication


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'status': forms.Select(),
        }



class EditCampagneForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'status': forms.Select(),
        }


class PubliciteForm(forms.ModelForm):
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all(),
        label="Sélectionner une campagne",
        required=True,
        widget=forms.Select
    )

    class Meta:
        model = Publicite
        fields = ['name', 'campaign', 'statut', 'budget_quotidien', 'objectif_optimisation', 'evenement_facturation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la publicité'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'budget_quotidien': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Budget quotidien'}),
            'objectif_optimisation': forms.Select(attrs={'class': 'form-control'}),
            'evenement_facturation': forms.Select(attrs={'class': 'form-control'}),
        }



# class PubliciteForm(forms.ModelForm):
#     class Meta:
#         model = Publicite
#         fields = ['name', 'statut', 'budget_quotidien','objectif_optimisation', 'evenement_facturation']
#         widgets = {
#
#             'statut': forms.Select(),
#             'objectif_optimisation': forms.Select(),
#             'evenement_facturation': forms.Select(),
#         }


class EditPudForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['name', 'statut', 'budget_quotidien',  'objectif_optimisation', 'evenement_facturation']
        widgets = {

            'statut': forms.Select(),
            'objectif_optimisation': forms.Select(),
            'evenement_facturation': forms.Select(),
        }

        
        

from django.forms import inlineformset_factory

class AudienceForm(forms.ModelForm):
    # Champ pour sélectionner des localisations existantes
    locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Affiche des cases à cocher pour chaque localisation
        required=True  # Le champ est facultatif
    )

    class Meta:
        model = Audience
        fields = ['name', 'age_min', 'age_max', 'interests', 'gender', 'locations']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['country', 'city',]

class PostPublicationForm(forms.ModelForm):
    class Meta:
        model = PostPublication
        fields = ['post_type', 'message', 'image', 'video', 'description']

    # Choix du type de publication (le même que dans le modèle)
    POST_TYPE_CHOICES = (
        ('message', 'Message'),
        ('image', 'Image'),
        ('video', 'Vidéo'),
    )

    post_type = forms.ChoiceField(label='Type de publication', choices=POST_TYPE_CHOICES)

    # Champs pour les différents types de publication
    message = forms.CharField(label='Message', max_length=255, widget=forms.Textarea, required=False)
    image = forms.ImageField(label='Sélectionner une image', required=False)
    video = forms.FileField(label='Sélectionner une vidéo', required=False)
    description = forms.CharField(label='Description', max_length=255, required=False)

    # Validation du formulaire en fonction du type de publication sélectionné
    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get('post_type')

        if post_type == 'message' and not cleaned_data.get('message'):
            self.add_error('message', 'Le message est obligatoire pour une publication de type message.')

        if post_type == 'image':
            if not cleaned_data.get('message'):
                self.add_error('message', 'Le message est obligatoire pour une publication de type image.')
            if not cleaned_data.get('image'):
                self.add_error('image', 'L\'image est obligatoire pour une publication de type image.')

        if post_type == 'video':
            if not cleaned_data.get('description'):
                self.add_error('description', 'La description est obligatoire pour une publication de type vidéo.')
            if not cleaned_data.get('video'):
                self.add_error('video', 'La vidéo est obligatoire pour une publication de type vidéo.')

        return cleaned_data
