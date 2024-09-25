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
        ('completed', 'desactiver'),
    ]

    name = models.CharField(max_length=200)
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
    ciblage = models.TextField(help_text="Détails concernant les critères de ciblage.",default='')
    objectif_optimisation = models.CharField(max_length=20, choices=OBJECTIFS_OPTIMISATION,default='')
    evenement_facturation = models.CharField(max_length=20, choices=EVENEMENTS_FACTURATION,default='')

    def __str__(self):
        return self.name


class Publicite(models.Model):
    name = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    # Champs de statut, objectifs et événements
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('mis_en_pause', 'Mis en pause'),
        ('termine', 'Terminé'),
    ]

    OBJECTIFS_OPTIMISATION_CHOICES = [
        ('clics_lien', 'Clics sur le lien'),
        ('impressions', 'Impressions'),
        ('engagement', 'Engagement'),
    ]

    EVENEMENTS_FACTURATION_CHOICES = [
        ('impressions', 'Impressions'),
        ('clics', 'Clics'),
    ]

    statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default='actif')
    budget_quotidien = models.DecimalField(max_digits=10, decimal_places=2)
    objectif_optimisation = models.CharField(max_length=20, choices=OBJECTIFS_OPTIMISATION_CHOICES)
    evenement_facturation = models.CharField(max_length=20, choices=EVENEMENTS_FACTURATION_CHOICES)

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





class PostPublication(models.Model):
    POST_TYPE_CHOICES = (
        ('message', 'Message'),
        ('image', 'Image'),
        ('video', 'Vidéo'),
    )

    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    id_publication = models.CharField(max_length=255,blank=True, null=True)  # Assurez-vous que cela est correct
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_type} - {self.id_publication}'





