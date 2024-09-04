from django import forms
from .models import Campagne,Audience, Interest, Location,Publicite



class CampagneForm(forms.ModelForm):
    create_ad = forms.BooleanField(required=False, label='Créer une publicité après avoir créé la campagne')

    class Meta:
        model = Campagne
        fields = ['nom', 'description', 'public_cible', 'budget', 'duree','objectifs']


class PubliciteForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['titre', 'description', 'type_contenu', 'fichier']  # Incluez tous les champs nécessaires
        
        
        



class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ['name', 'description', 'age_min', 'age_max', 'gender', 'interests', 'location']

    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Centres d'intérêt"
    )

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label="Localisation"
    )

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'country', 'region', 'city']