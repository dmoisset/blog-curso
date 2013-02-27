import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

ZODIAC_SIGN_CHOICES = (
    ('AR', 'Aries'),
    ('TA', 'Taurus'),
    ('GE', 'Gemini'),
    ('CA', 'Cancer'),
    ('LE', 'Leo'),
    ('VI', 'Virgo'),
    ('LI', 'Libra'),
    ('SC', 'Scorpio'),
    ('SA', 'Sagittarius'),
    ('CP', 'Capricorn'),
    ('AQ', 'Aquarius'),
    ('PI', 'Pisces'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    zodiac_sign = models.CharField(max_length=2, choices=ZODIAC_SIGN_CHOICES)
    favorite_color = models.CharField(max_length=25, default="Green.")


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
