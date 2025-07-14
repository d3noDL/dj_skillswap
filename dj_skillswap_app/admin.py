from django.contrib import admin
from .models import Skill, UserProfile, UserProfileSkill, Category

admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(UserProfileSkill)
admin.site.register(Category)
