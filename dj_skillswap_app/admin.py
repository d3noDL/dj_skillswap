from django.contrib import admin
from dj_skillswap_app.models import Skill
from .models import Profile

admin.site.register(Skill)
admin.site.register(Profile)