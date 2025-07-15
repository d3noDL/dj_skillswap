from django import forms
from .models import Category, Skill, UserProfile, UserProfileSkill, Message, Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'bio', 'profile_picture']
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
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Category",
    )

    class Meta:
        model = UserProfileSkill
        fields = ('category', 'skill',  'avaliability',
                  'description', 'type', 'pitch', 'status')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # get user from view
        super().__init__(*args, **kwargs)

        # 1. if editing an existing skill
        if self.instance and self.instance.pk:
            skill = self.instance.skill
            self.fields['category'].initial = skill.category
            self.fields['skill'].queryset = Skill.objects.filter(
                category=skill.category)
        # 2. if creating a new skill
        elif 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['skill'].queryset = Skill.objects.filter(
                    category_id=category_id)
            except (ValueError, TypeError):
                self.fields['skill'].queryset = Skill.objects.none()
        else:
            self.fields['skill'].queryset = Skill.objects.none()

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("user_receiver", "subject", "message")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("rating_receiver", "rating", "comment")