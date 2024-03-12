from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # Ajoutez d'autres champs de profil si nécessaire

    def __str__(self):
        return f"{self.user.username}'s Profile"