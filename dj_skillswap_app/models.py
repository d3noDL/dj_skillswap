from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"Skill: {self.name} in the category :{self.category}"


class UserProfileSkill(models.Model):
    class TypePosting(models.TextChoices):
        OFFER = 'Offer', 'Offer'
        REQUEST = 'Request', 'Request'

    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    type = models.CharField(
        max_length=20, choices=TypePosting.choices, default=TypePosting.OFFER)
    avaliability = models.CharField(max_length=250)
    pitch = models.CharField(max_length=140)
    created_at = models.DateTimeField(
        auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  
        


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    picture = models.ImageField(
        upload_to='userprofile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', through='UserProfileSkill')
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    

    def __str__(self):       
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name 

    def is_complete(self):
        return bool(self.bio.strip())
