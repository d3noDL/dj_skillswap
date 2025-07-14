from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dj_skillswap_app.models import UserProfileSkill


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddProfileSkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # get user from view
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfileSkill
        fields = ('profile', 'skill', 'avaliability',
                  'description', 'type', 'pitch', 'status')
