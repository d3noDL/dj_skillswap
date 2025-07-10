from django import forms
from dj_skillswap_app.models import Skill, Message

class AddSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ("__all__")

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("user_receiver", "subject", "message")