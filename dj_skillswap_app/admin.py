from django.contrib import admin
from .models import Skill, UserProfile, UserProfileSkill, Category, Message

admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(UserProfileSkill)
admin.site.register(Category)
admin.site.register(Message)
