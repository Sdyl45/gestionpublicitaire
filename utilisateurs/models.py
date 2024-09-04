from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


ROLES = [
    ('admin', 'Administrateur'),
    ('chef_services', 'Chef services'),
    ('directeur_marketing', 'DirecteurMarketing'),
    ('commercial', 'commerciaux'),

]


class Utilisateur(AbstractUser):
    role = models.CharField(choices=ROLES, max_length=255)
