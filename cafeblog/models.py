from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

TITLE_MAX_LEN = 250

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

class Blog(models.Model):
    """A Blog to post articles"""
    title = models.CharField(max_length=TITLE_MAX_LEN, unique=True)
    description = models.TextField(blank=True)
    administrator = models.ForeignKey(User, related_name='admin') #6
    authors = models.ManyToManyField(User) #6
    #tags = #8

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cafeblog:detail', kwargs={'blog_pk': self.pk})


class Article(models.Model):
    """An article in some blog"""
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=TITLE_MAX_LEN)
    contents = models.TextField()
    author = models.ForeignKey(User)
    creation_time = models.DateTimeField()
    pub_date = models.DateTimeField("date published", blank=True, null=True)
    last_modified = models.DateTimeField()
    is_published = models.BooleanField()

    def __unicode__(self):
        return self.title


    class Meta:
        ordering = ['-pub_date']
        order_with_respect_to = 'blog'
        unique_together = [("blog", "title")]
