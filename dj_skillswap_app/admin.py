from django.contrib import admin
from dj_skillswap_app.models import Skill
from .models import UserProfile



admin.site.register(Skill)
admin.site.register(UserProfile)
