from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class ProfileSkill(models.Model):
    class TypePosting(models.TextChoices):
        OFFER = 'Offer', 'Offer'
        REQUEST = 'Request', 'Request'

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    type = models.CharField(
        max_length=20, choices=TypePosting.choices, default=TypePosting.OFFER)
    avaliability = models.CharField(max_length=250)
    pitch = models.CharField(max_length=140)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', through='ProfileSkill')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
