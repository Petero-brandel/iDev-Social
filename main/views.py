from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, ProfileUpdateForm, CreatePostForm
from .models import Profile, Project
from django.core.exceptions import ValidationError


# Authentication and Authorization Views

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                # login(request, user) # Uncomment to log in after signup
                return redirect('/login')
        except ValidationError as e:
            form.add_error('email', e)  # Add email-specific error to the form
    else:
        form = SignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')

# Feed and Home Views
@login_required(login_url='/login')
def feed(request):
    return render(request, 'main/feed.html', {'feed': feed})

def home(request):
    return render(request, 'main/home.html', {'home': home})

# Profile Related Views
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_user = user.profile
    projects = user.projects.all()  # Get user's posts/projects
    context = {
        'user': user,
        'profile_user': profile_user,
        'projects': projects,
    }
    return render(request, 'main/profilepage.html', context)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow.profile.followers.filter(id=request.user.id).exists():
        # Unfollow user
        user_to_follow.profile.followers.remove(request.user)
        request.user.profile.following.remove(user_to_follow)
    else:
        # Follow user
        user_to_follow.profile.followers.add(request.user)
        request.user.profile.following.add(user_to_follow)
    
    return redirect('profile', username=user_to_follow.username)

@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileUpdateForm(instance=user.profile)
    
    return render(request, 'main/edit_profile.html', {'form': form})

# Signals for automatic profile creation and email uniqueness
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from django.urls import reverse

@login_required
def add_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)  
            project.user = request.user  
            project.save()  
            return redirect(reverse('profile', args=[request.user.username]))  
    else:
        form = CreatePostForm()
    return render(request, 'main/projects_form.html', {'form': form})
