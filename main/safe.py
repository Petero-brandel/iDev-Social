# To add "likes" and "comments" functionality to your Django project, follow the steps below. This will involve:

# 1. Creating models for likes and comments.
# 2. Modifying the templates to show likes and comments.
# 3. Adding views for submitting likes and comments.
# 4. Updating URLs to handle likes and comments.

# ### Step 1: Update the Models

# You will need to add two models: one for likes and one for comments. These models will link to the `Project` model you already have.

#### Models: `Like` and `Comment`

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} liked {self.project.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} commented on {self.project.title}"
# ```

# - The `Like` model connects a user to a project and stores the timestamp when the like occurred.
# - The `Comment` model stores the user, project, comment text, and the time it was created.

# ### Step 2: Create Forms for Comments

# You need to create a form for users to submit comments. In `forms.py`, create a `CommentForm`.

# #### `forms.py`
# ```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
# ```

# ### Step 3: Update Views for Likes and Comments

# You’ll need two views: one for handling likes and another for handling comment submissions.

# #### Views: Handling Likes and Comments

# ```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Like, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def like_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, project=project)
    if not created:
        # If the like already exists, unlike the project
        like.delete()
    return redirect('profile', username=project.user.username)

@login_required
def add_comment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()
            return redirect('profile', username=project.user.username)
    else:
        form = CommentForm()
    
    return render(request, 'project_detail.html', {'project': project, 'form': form})
# ```

# - **`like_project`**: This view allows users to like or unlike a project.
# - **`add_comment`**: This view allows users to submit comments.

# ### Step 4: Modify the Template to Display Likes and Comments

# In your project template, display the like button, number of likes, and comments. Also, include a form for submitting comments.

# #### `project_detail.html` (or within the profile page)
# ```html
<div class="project">
    <!-- Existing project info -->
    <h3>{{ project.title }}</h3>
    <img src="{{ project.image.url }}" alt="Project image">
    
    <p>{{ project.description }}</p>
    <p>Built with: {{ project.UsedLanguage }}</p>
    
    <!-- Like and Comment Features -->
    <div class="project-actions">
        <!-- Like Button -->
        <form action="{% url 'like_project' project.pk %}" method="POST">
            {% csrf_token %}
            <button type="submit">
                {% if user in project.likes.all %}
                    Unlike
                {% else %}
                    Like
                {% endif %}
            </button>
        </form>
        <p>{{ project.likes.count }} likes</p>

        <!-- Comments Section -->
        <h4>Comments:</h4>
        <ul>
            {% for comment in project.comments.all %}
                <li><strong>{{ comment.user.username }}:</strong> {{ comment.comment }} ({{ comment.created_at|timesince }} ago)</li>
            {% empty %}
                <li>No comments yet.</li>
            {% endfor %}
        </ul>
        
        <!-- Add a Comment -->
        <form action="{% url 'add_comment' project.pk %}" method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Add Comment</button>
        </form>
    </div>
</div>
```

# This template will:
# - Show a "Like" or "Unlike" button based on whether the user has already liked the project.
# - Display the total number of likes.
# - Show all comments for the project.
# - Provide a form for adding a new comment.

# ### Step 5: Add URLs for Likes and Comments

# In your `urls.py`, define the URLs for liking and commenting.

# #### `urls.py`
# ```python
from django.urls import path
from . import views

urlpatterns = [
    # Other URLs
    path('like_project/<int:pk>/', views.like_project, name='like_project'),
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
]
# ```

# ### Step 6: Migrate the Changes

# Run the necessary migrations for your new models and changes:

# ```bash
# python manage.py makemigrations
# python manage.py migrate
# ```

# ### Step 7: Styling (Optional)

# Add CSS to style the like button, comment form, and comment section in your `styles.css`.

# ### Conclusion

# This setup allows users to:
# - Like or unlike projects.
# - Post comments on projects.
# - View the number of likes and all the comments for a project.

# If you want to show who liked the project or add further notification functionality, you can expand on this by integrating Django signals and notifications packages.






Let's walk through the likes, comments, and posting functionality in Django step-by-step, with detailed explanations for each part of the process. I'll start with the Django basics and then move into the details of each feature.

1. Models (Database Structure)
The models define the structure of your database. You create models for posts, comments, likes, and users.

python
Copy code
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} likes {self.post.content[:20]}"
Explanation:
Post Model:
user = models.ForeignKey(User, on_delete=models.CASCADE): This creates a relationship between a post and a user. It means each post belongs to a user, and when the user is deleted, their posts are also deleted (on_delete=models.CASCADE).
content = models.TextField(): This field will store the text content of the post.
created_at = models.DateTimeField(auto_now_add=True): Automatically sets the time when the post is created.
Comment Model:
post = models.ForeignKey(Post, on_delete=models.CASCADE): Links each comment to a post. If the post is deleted, the related comments are deleted as well.
user = models.ForeignKey(User, on_delete=models.CASCADE): Links each comment to a user.
content = models.TextField(): Stores the text content of the comment.
created_at = models.DateTimeField(auto_now_add=True): Automatically sets the time when the comment is created.
Like Model:
post = models.ForeignKey(Post, on_delete=models.CASCADE): Links each like to a specific post.
user = models.ForeignKey(User, on_delete=models.CASCADE): Links each like to a user.
created_at = models.DateTimeField(auto_now_add=True): Automatically sets the time when the like is created.
2. Views (Handling User Requests)
The views in Django handle user requests, like adding a post, liking a post, or adding a comment.

python
Copy code
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from django.contrib.auth.decorators import login_required


Explanation:
add_post view:

@login_required: This ensures that only logged-in users can access this view.
if request.method == 'POST': We check if the method of the request is POST, which means the user is submitting the form to add a post.
content = request.POST.get('content'): Retrieves the content of the post from the form.
Post.objects.create(user=request.user, content=content): Creates a new post linked to the logged-in user.
like_post view:

get_object_or_404(Post, id=post_id): This retrieves the post or raises a 404 error if the post does not exist.
if Like.objects.filter(post=post, user=request.user).exists(): Checks if the user has already liked the post. If they have, it deletes the like; if not, it creates a new like.
add_comment view:

Similar to the add_post view, but this one handles comments on a specific post.
3. URLs (Routing User Requests)
You need to define routes to connect the views with the URLs.

python
Copy code
from django.urls import path
from . import views

urlpatterns = [
    
]
Explanation:
path('add_post/', views.add_post, name='add_post'): This maps the URL /add_post/ to the add_post view.
path('like_post/<int:post_id>/', views.like_post, name='like_post'): This maps the URL /like_post/<post_id>/ to the like_post view. The <int:post_id> part allows us to pass the post's ID to the view.
path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'): This does the same for adding comments.
4. Templates (Displaying Data)
Templates are responsible for rendering HTML to the user.

html
Copy code

Explanation:
{% for post in posts %}: Loops through each post passed to the template.
post.likes.count: Displays the number of likes a post has. We use .count() to get the total number of likes.
{% for comment in post.comments.all %}: Loops through the comments related to the post and displays them.
Additional Knowledge
CSRF Token: Django automatically includes protection against cross-site request forgery (CSRF) attacks using {% csrf_token %}. This token ensures that forms submitted come from the correct user and not from an attacker.

Database Relationships:

ForeignKey: Used to define a many-to-one relationship. For example, a post can have many comments, but a comment belongs to one post.
related_name: This defines a reverse relationship. When you use related_name='comments' in the Comment model, you can access the comments for a post by calling post.comments.all().
Django ORM (Object-Relational Mapping):

This allows you to interact with your database using Python code, without writing raw SQL queries. For example, Post.objects.create() creates a new post in the database.
This is a high-level explanation of how Django works for posts, likes, and comments. Let me know if you need more clarification on specific parts!















from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, ProfileUpdateForm, CreatePostForm, CreateProjectForm
from .models import Profile, Project, Post, Comment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse


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
    # Retrieve all posts from the database
    posts = Post.objects.all().order_by('-created_at')  
    return render(request, 'main/feed.html', {'posts': posts})

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
def project_upload(request):
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
        Profile.objects.get_or_create(user=instance)


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





@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user has already liked the post
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike the post
    else:
        post.likes.add(request.user)  # Like the post

    return redirect('feed')  # Redirect back to the feed or the same page




@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and len(content.strip()) > 0:  # Prevent adding empty comments
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('feed')



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


#deleting post


@login_required
def delete_post(request, post_id):
    # Get the post by id, ensuring that the user is the owner of the post
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post.delete()  # Delete the post from the database
        messages.success(request, 'Post deleted successfully.')  # Flash a success message
    
    return redirect('feed')  # Redirect back to the feed after deletion
