import datetime
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Avg
from django.contrib.auth.models import User

class Blog(models.Model):
    """A Blog to post stuff"""
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    administrator = models.ForeignKey(User, related_name='admin') #6
    authors = models.ManyToManyField(User) #6
    #tags = #8

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cafeblog:detail', kwargs={'blog_pk': self.pk})
