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
        fields = ['name', 'statut', 'budget_quotidien', 'ciblage', 'objectif_optimisation', 'evenement_facturation']
        widgets = {
            'ciblage': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'statut': forms.Select(),
            'objectif_optimisation': forms.Select(),
            'evenement_facturation': forms.Select(),
        }


class EditPudForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['name', 'statut', 'budget_quotidien', 'ciblage', 'objectif_optimisation', 'evenement_facturation']
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





class FacebookPostForm(forms.Form):
    POST_TYPE_CHOICES = (
        ('message', 'Message'),
        ('image', 'Image'),
        ('video', 'Vidéo'),
    )

    post_type = forms.ChoiceField(label='Type de publication', choices=POST_TYPE_CHOICES)
    message = forms.CharField(label='Message', max_length=255, widget=forms.Textarea, required=False)
    image = forms.ImageField(label='Sélectionner une image', required=False)
    video = forms.FileField(label='Sélectionner une vidéo', required=False)
    description = forms.CharField(label='Description', max_length=255, required=False)

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