from django import forms
from dj_skillswap_app.models import ProfileSkill


class AddProfileSkillForm(forms.ModelForm):
    class Meta:
        model = ProfileSkill
        fields = ('profile', 'skill', 'avaliability', 'description', 'type', 'pitch')
