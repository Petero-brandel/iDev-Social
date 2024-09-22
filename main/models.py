from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    github = models.CharField(max_length=225)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    UsedLanguage = models.TextField(max_length=225, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='project_pics')
    postime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

