from django import forms
from .models import Campagne,Audience, Interest, Location

class CampagneForm(forms.ModelForm):
    class Meta:
        model = Campagne
        fields = ['name', 'description', 'start_date', 'end_date', 'budget']
        
        
        



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