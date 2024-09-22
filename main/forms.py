from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Project

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
        fields = ['bio', 'github', 'image', 'cover_photo']  # Include any fields you want to allow users to update
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        
class CreatePostForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'UsedLanguage', 'url', 'image')
        labels = {
            'title': 'Enter Your Title here',
            'description': 'Briefly Describe what your Project is all about',
            'UsedLanguage': 'What Languages Did you Use',
            'url': 'What Languages Did you Use',
            'image': 'Upload Your Design Image here'
        }
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter a Title'}),
            'description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter a Title'}),
            'UsedLanguage' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter a Title'}),
            'url' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'enter a link to your project (website/github)'}),
            
           
            
        }