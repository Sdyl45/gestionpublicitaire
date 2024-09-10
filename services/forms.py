from django import forms
from .models import Campaign,Audience, Interest, Location,Publicite



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
    class Meta:
        model = Publicite
        fields = ['nom', 'statut', 'budget_quotidien', 'ciblage', 'objectif_optimisation', 'evenement_facturation']
        widgets = {
            'ciblage': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'statut': forms.Select(),
            'objectif_optimisation': forms.Select(),
            'evenement_facturation': forms.Select(),
        }


class EditPudForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['nom', 'statut', 'budget_quotidien', 'ciblage', 'objectif_optimisation', 'evenement_facturation']
        widgets = {
            'ciblage': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'statut': forms.Select(),
            'objectif_optimisation': forms.Select(),
            'evenement_facturation': forms.Select(),
        }

        
        



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