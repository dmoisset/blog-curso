import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    biography = models.TextField(blank=True)
    photo = models.FileField(upload_to="profile_pictures", blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
