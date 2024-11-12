from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, ProfileUpdateForm, CreatePostForm, CreateProjectForm, CreateGroupForm
from .models import Profile, Project, Post, Comment, Like, Group, Conversations
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse


# Authentication and Authorization Views

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        try:
            if form.is_valid():
                form.save()
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
    # Retrieve all posts from the database
    group = Group.objects.all()
    posts = Post.objects.all().order_by('-created_at')  
    return render(request, 'main/feed.html', {'posts': posts, 'groups' : group})

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


#learning pageview

@login_required
def learn(request):
    
    return render(request, 'main/learnpage.html', {})


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
def add_friend(request, user_id):
    friend_to_add = get_object_or_404(User, id=user_id)
    if friend_to_add.profile.friends.filter(id=request.user.id).exists():
        friend_to_add.profile.friend.add(request.user)
        request.user.profile.friend.add(friend_to_add)
        
    return redirect('profile', username=friend_to_add.username)

# home page render view
def home(request):
    return render(request, 'main/home.html', {'home': home})



# project upload and related

@login_required
def project_upload(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)  
            project.user = request.user  
            project.save()  
            return redirect(reverse('profile', args=[request.user.username]))  
    else:
        form = CreateProjectForm()
    return render(request, 'main/projects_form.html', {'form': form})


@login_required
def delete_project(request, project_id):
    # Get the post by id, ensuring that the user is the owner of the post
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        project.delete()  # Delete the post from the database
        messages.success(request, 'Post deleted successfully.')  # Flash a success message
    
        return redirect(reverse('profile', args=[request.user.username]))

# creating post ------------->
#creating a post ------>
@login_required
def add_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Save the form but don't commit it yet
            post.user = request.user  # Assign the current user to the post
            post.save()  # Now save it in the database
            return redirect('feed')
    else:
        form = CreatePostForm()
    return render(request, 'main/post_form.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        # If the like already exists, unlike the post
        like.delete()
    return redirect('feed')



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and len(content.strip()) > 0:  # Prevent adding empty comments
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('/feed')


#deleting post
@login_required
def delete_post(request, post_id):
    # Get the post by id, ensuring that the user is the owner of the post
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post.delete()  # Delete the post from the database
        messages.success(request, 'Post deleted successfully.')  # Flash a success message
    
    return redirect('/feed')  # Redirect back to the feed after deletion



# # Creating groups function =====================>
# @login_required
# def create_group(request):
#     form = CreateGroupForm()
#     if request.method == 'POST':
#         form = CreateGroupForm(request.POST)
#         if form.is_valid():
            
#             group = form.save(commit=False)
#             # Assign the logged-in user as the host
#             group.host = request.user
#             group.save()  #  save the group to the database
#             group.participants.add(group.host)
#             return redirect('/feed')
#     return render(request, 'main/create_group_form.html', {'form': form})


def group_details(request, pk):
    group = get_object_or_404(Group, id=pk,)
    conversations = Conversations.objects.filter(group=group)
    participants = group.participants.all().filter(group=group)
    if request.method =='POST':
        message = request.POST.get('body')
        conversations = Conversations.objects.create(
            user=request.user,
            group=group,
            body=message
        )
        return redirect('group-in', pk=group.id)
    context = {
        'group':group,
        'conversations':conversations,
        'participants': participants,
    }

    return render(request, 'main/group_details.html', context)  


@login_required
def join_group(request, pk):
    group = get_object_or_404(Group, pk=pk)  # Fetch the group by primary key (pk)
    
    if request.method == 'POST':
        group.participants.add(request.user)  # Add the user to the participants
        return redirect('group-in', pk=group.id)  # Redirect to the group details view
    
    # Optionally handle GET if needed
    return redirect('feed')  # Redirect to feed or any other page


@login_required
def delete_group(request, pk):
   
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        group.delete()  
        messages.success(request, 'group deleted successfully.') 
    
    return redirect('/feed') 

# @login_required
# def edit_group(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     if request.method == 'POST':
#         form = GroupUpdateForm(request.POST, request.FILES, instance=group)
#         if form.is_valid():
#             form.save()
#             return redirect()
#     else:
#         group = ProfileUpdateForm(instance=group)
    
#     return render(request, 'main/edit_profile.html', {'form': form})

@login_required
@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Use request.FILES for the image field

        # Create a new Group instance
        group = Group(host=request.user, name=name, description=description, image=image)
        group.save()
        
        # Add the user as a participant
        group.participants.add(group.host)
        
        # Redirect to the feed page
        return redirect('/feed')
    
    return render(request, 'main/group_details.html')