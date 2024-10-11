from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, default='username')
    bio = models.TextField(max_length=500, blank=True)
    github = models.CharField(max_length=225, default='https://github.com/')
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    friends = models.ManyToManyField(User, related_name='my_friend', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.profile.name


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    UsedLanguage = models.TextField(max_length=225, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='project_pics', default='default.jpg')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='project_pics', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s post"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} liked {self.project.title}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]
    
    

        
        
        
# rooms model ================>

class Topic(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    #participants =
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
        
    def __str__(self):
        return self.name    

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    