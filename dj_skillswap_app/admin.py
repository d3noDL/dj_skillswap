from django.contrib import admin
from .models import Profile, Skill, ProfileSkill

admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(ProfileSkill)
