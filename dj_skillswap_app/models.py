from django.db import models
from django.contrib.auth.models import User 

class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"Skill: {self.name} in the category :{category}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills_offered = models.TextField(blank=True)
    skills_needed = models.TextField(blank=True)

    def __str__(self):
        return self.user.username