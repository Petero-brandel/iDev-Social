from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Project, Post, Room

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}))
    github = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))
    agree_terms = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'label': 'I agree to the terms and conditions'}),)

    class Meta:
        model = User
        fields = ['username', 'email', 'github', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'github', 'image', 'cover_photo', 'name']  # Include any fields you want to allow users to update
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'name': forms.Textarea(attrs={'rows': 1}),
        }
        
class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'UsedLanguage', 'url', 'image')
        labels = {
            'title': 'Enter Your Project Title:',
            'description': 'Briefly Describe what your Project is all about:',
            'UsedLanguage': 'Language/Framework(s):',
            'url': 'Link to Project:',
            'image': 'Upload Your Design Image here'
        }
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : ''}),
            'description': forms.Textarea(attrs={'rows': 8}),
            'UsedLanguage' : forms.TextInput(attrs={'class' : 'textarea-field', 'class' : 'form-control', 'placeholder' : 'e.g php, python, etc'}),
            'url' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'enter a link to your project (website/github)'}),
                 
        }
        
        #adding Post ------------>
        
class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image')
        label ={
            'content' : '',
            'image' : 'Upload an Image'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }
        
        
        # create room forms============>

class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'topic', 'description')