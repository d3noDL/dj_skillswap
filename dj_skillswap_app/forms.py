from django import forms
from dj_skillswap_app.models import UserProfileSkill


class AddProfileSkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # get user from view
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfileSkill
        fields = ('profile', 'skill', 'avaliability',
                  'description', 'type', 'pitch')
