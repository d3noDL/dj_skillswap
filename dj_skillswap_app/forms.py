from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'skills_offered', 'skills_needed']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'skills_offered': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What can you offer?'}),
            'skills_needed': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What skills are you looking for?'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
