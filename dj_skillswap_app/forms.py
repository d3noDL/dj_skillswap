from django import forms
from .models import Category, Skill, UserProfile, UserProfileSkill, Message, Rating
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('firstname', placeholder='Your first name'),
            Field('lastname', placeholder='Your last name'),
            Field('bio'),
            Field('profile_picture'),
            Submit('submit', 'Save Profile', css_class='btn btn-primary mt-3')
        )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', placeholder='Pick a username'),
            Field('email', placeholder='Your email address'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Confirm password'),
            Submit('submit', 'Sign Up', css_class='btn btn-success mt-3')
        )


class AddProfileSkillForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Category")

    class Meta:
        model = UserProfileSkill
        fields = ('category', 'skill', 'avaliability', 'description', 'type', 'pitch', 'status')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=[
            (True, 'Active'),
            (False, 'Inactive')
        ])
        self.fields['description'].widget = Textarea(attrs={
            'placeholder': 'Describe the swap',
            'rows': 4,  
        })

        # dynamic skill queryset logic as before
        if self.instance.pk:
            skill = self.instance.skill
            self.fields['category'].initial = skill.category
            self.fields['skill'].queryset = Skill.objects.filter(category=skill.category)
        elif 'category' in self.data:
            try:
                cat_id = int(self.data.get('category'))
                self.fields['skill'].queryset = Skill.objects.filter(category_id=cat_id)
            except (ValueError, TypeError):
                self.fields['skill'].queryset = Skill.objects.none()
        else:
            self.fields['skill'].queryset = Skill.objects.none()

        # Crispy layout for Bootstrap styling + placeholders
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('type', placeholder='Offer or Request'),
            Field('category', placeholder='Select category'),
            Field('skill', placeholder='Select skill'),
            Field('avaliability', placeholder='e.g. Weekends'),
            Field('pitch', placeholder='Your pitch'),
            Field('description', placeholder='Describe the swap'),          
            Field('status', placeholder='e.g. Open'),
            Submit('submit', 'Save', css_class='btn btn-primary mt-3')
        )

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "message")
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write your message here...",
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field("subject"),
            Field("message", wrapper_class="mb-3"),
            Submit("submit", "Submit Review", css_class="btn btn-primary w-100 d-flex")
        )



class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.HiddenInput())  # usamos apenas as estrelas no HTML

    class Meta:
        model = Rating
        fields = ( "rating", "comment")
        widgets = {
            "comment": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Leave a comment here...",
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field("rating", css_id="rating-input"),  # input hidden
            Field("comment", wrapper_class="mb-3"),
            Submit("submit", "Submit Review", css_class="btn btn-primary w-100")
        )
