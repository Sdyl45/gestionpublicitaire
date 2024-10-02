from django.db import models
from django import forms
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db import models



class Campaign(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activer'),
        ('paused', 'Suspendu'),
        ('ARCHIVED', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    facebookCampaign_ID = models.CharField(max_length=200,default='',null=False)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='desactiver')

    def __str__(self):
        return self.name




class Publicite(models.Model):
    STATUT_CHOIX = [
        ('actif', 'Actif'),
        ('mis_en_pause', 'Mis en pause'),
        ('termine', 'Terminé'),
    ]

    OBJECTIFS_OPTIMISATION = [
        ('clics_lien', 'Clics sur le lien'),
        ('impressions', 'Impressions'),
        ('engagement', 'Engagement'),
    ]

    EVENEMENTS_FACTURATION = [
        ('impressions', 'Impressions'),
        ('clics', 'Clics'),
    ]

    name = models.CharField(max_length=200,default='')
    statut = models.CharField(max_length=12, choices=STATUT_CHOIX, default='actif')
    budget_quotidien = models.DecimalField(max_digits=10, decimal_places=2,default='' )
    objectif_optimisation = models.CharField(max_length=20, choices=OBJECTIFS_OPTIMISATION,default='')
    evenement_facturation = models.CharField(max_length=20, choices=EVENEMENTS_FACTURATION,default='')

    def __str__(self):
        return self.name




class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.city}, {self.country}"


class Audience(models.Model):
    name = models.CharField(max_length=100)
    age_min = models.IntegerField()
    age_max = models.IntegerField()
    interests = models.TextField()
    gender = models.CharField(max_length=10)

    # Ajout du ManyToManyField pour associer plusieurs localisations
    locations = models.ManyToManyField(Location, blank=True)

    def __str__(self):
        return self.name





from django.db import models
from django.conf import settings

class PostPublication(models.Model):
    POST_TYPE_CHOICES = (
        ('message', 'Message'),
        ('image', 'Image'),
        ('video', 'Vidéo'),
    )
    id_publication = models.CharField(max_length=255,primary_key=True)  # Assurez-vous que cela est correct
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_type} - {self.id_publication}'





class Like(models.Model):
    post = models.ForeignKey(PostPublication, related_name='likes', on_delete=models.CASCADE)  # Utiliser 'likes' comme related_name
    liker_id = models.CharField(max_length=255)  # ID de l'utilisateur qui a liké depuis Facebook
    liker_name = models.CharField(max_length=255)  # Nom de l'utilisateur qui a liké

    def __str__(self):
        return f'Like by {self.liker_name} on {self.post_type}'


class Comment(models.Model):
    post = models.ForeignKey(PostPublication, on_delete=models.CASCADE)
    comment_id = models.CharField(max_length=255)
    message = models.TextField()
    commenter_name = models.CharField(max_length=255)
    created_time = models.DateTimeField()



class BoostedPost(models.Model):
    post_id = models.CharField(max_length=100)
    page_id = models.CharField(max_length=100)
    ad_set_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def stop_boost(self):
        # Logique pour arrêter le boost via l'API Facebook
        pass

    def delete_boost(self):
        # Logique pour supprimer la publication boostée via l'API Facebook
        pass
    def __str__(self):
        return self.posted_by






class FacebookPostInfo(models.Model):
    post_id = models.CharField(max_length=255)  # ID de la publication Facebook
    posted_by = models.CharField(max_length=255)  # Nom de l'utilisateur qui a posté
    created_time = models.DateTimeField()  # Date de création de la publication
    message = models.TextField()  # Message de la publication
    likes_count = models.IntegerField(default=0)  # Nombre de likes
    comments_count = models.IntegerField(default=0)  # Nombre de commentaires
    comment_id = models.CharField(max_length=255, blank=True, null=True)  # ID du commentaire
    like_id = models.CharField(max_length=255, blank=True, null=True)  # ID du like

    def __str__(self):
        return f"Post ID: {self.post_id} by {self.posted_by}"
