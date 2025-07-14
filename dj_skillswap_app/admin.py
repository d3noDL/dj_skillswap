from django.contrib import admin
from .models import Skill, UserProfile, UserProfileSkill

admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(UserProfileSkill)
