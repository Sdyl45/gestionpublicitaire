from django.db import models
from django import forms
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


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
    id_publication = models.CharField(max_length=255, unique=True)
    post_type = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    # Changer les noms des relations pour éviter les conflits
    post_likes = models.ManyToManyField('Like', related_name='liked_publications', blank=True)
    post_comments = models.ManyToManyField('Comment', related_name='commented_publications', blank=True)

    def __str__(self):
        return self.message or "Publication sans message"

    def update_like_and_comment_counts(self):
        """
        Met à jour les attributs like_count et comment_count en fonction du nombre de likes et de commentaires liés.
        """
        # Utilisation des méthodes des classes Like et Comment
        self.like_count = Like.count_likes_for_post(self.id_publication)
        self.comment_count = Comment.count_comments_for_post(self.id_publication)
        self.save()  # Sauvegarde les modifications dans la base de données


class Like(models.Model):
    liker_id = models.CharField(max_length=255)
    liker_name = models.CharField(max_length=255)

    # Changer le related_name pour éviter les conflits
    post = models.ForeignKey(PostPublication, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liker_name} a aimé la publication {self.post.id_publication}"

    @classmethod
    def count_likes_for_post(cls, post_id):
        """
        Compte le nombre total de likes associés à une publication donnée.
        """
        return cls.objects.filter(post__id_publication=post_id).count()

class Comment(models.Model):
    comment_id = models.CharField(max_length=255, unique=True)
    message = models.TextField()
    commenter_name = models.CharField(max_length=255)
    created_time = models.DateTimeField()

    # Changer le related_name pour éviter les conflits
    post = models.ForeignKey(PostPublication, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.commenter_name} a commenté : {self.message}"

    @classmethod
    def count_comments_for_post(cls, post_id):
        """
        Compte le nombre total de commentaires associés à une publication donnée.
        """
        return cls.objects.filter(post__id_publication=post_id).count()

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




class CommentReply(models.Model):
    comment_id = models.CharField(max_length=255)
    reply_message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Réponse de {self.user} au commentaire {self.comment_id}"