from django import forms
from dj_skillswap_app.models import Skill

class AddSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ("__all__")