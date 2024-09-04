from django.db import models
from django import forms
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser





class Campagne(models.Model):
    nom = models.CharField(max_length=200, null=True)
    description = models.TextField()
    public_cible = models.CharField(
        max_length=20,
        choices=[
            ('adults', 'Adultes'),
            ('teenagers', 'Adolescents'),
            ('seniors', 'Seniors'),
        ],
        null=True  # Permettre des valeurs nulles
    )

    OBJECTIFS_CHOICES = [
        ('conversions', 'Conversions'),
        ('trafic', 'Trafic'),
        ('engagement', 'Engagement'),
        ('vues_video', 'Vues vidéo'),
    ]

    objectifs = models.CharField(
        max_length=50,
        choices=OBJECTIFS_CHOICES,
        null=True  # Permettre des valeurs nulles
    )

    budget = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.PositiveIntegerField(default=0)  # Durée en jours

    def __str__(self):
        return self.nom


from django.db import models

class Publicite(models.Model):
    TYPE_CONTENU_CHOICES = [
        ('video', 'Vidéo'),
        ('image', 'Image'),
        ('texte', 'Texte'),
    ]

    titre = models.CharField(max_length=255)
    description = models.TextField()
    type_contenu = models.CharField(max_length=20, choices=TYPE_CONTENU_CHOICES)
    fichier = models.FileField(upload_to='publicites/', null=True, blank=True)

    def __str__(self):
        return self.titre


class Audience(models.Model):
    """
    Modèle représentant une audience pour une publicité.
    """
    name = models.CharField(max_length=100, verbose_name="Nom de l'audience")
    description = models.TextField(verbose_name="Description de l'audience", blank=True, null=True)
    age_min = models.PositiveIntegerField(verbose_name="Âge minimum", default=18)
    age_max = models.PositiveIntegerField(verbose_name="Âge maximum", default=65)
    gender = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin'), ('O', 'Autre')], verbose_name="Sexe")
    interests = models.ManyToManyField('Interest', related_name='audiences', verbose_name="Centres d'intérêt")
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='audiences', verbose_name="Localisation")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return self.name



class Interest(models.Model):
    """
    Modèle représentant un centre d'intérêt pour une audience.
    """
    name = models.CharField(max_length=100, verbose_name="Nom du centre d'intérêt")

    def __str__(self):
        return self.name

class Location(models.Model):
    """
    Modèle représentant une localisation pour une audience.
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la localisation")
    country = models.CharField(max_length=100, verbose_name="Pays")
    region = models.CharField(max_length=100, verbose_name="Région", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.country}"