from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    skills_offered = models.CharField(max_length=255, blank=True)
    skills_needed = models.CharField(max_length=255, blank=True)

    skills = models.ManyToManyField('Skill', through='UserProfileSkill')

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name

    def is_complete(self):
        return bool(self.firstname .strip() and self.lastname.strip() and self.bio.strip())

class Message(models.Model):
    user_sender = models.ForeignKey(UserProfile, related_name="user_sender", on_delete=models.CASCADE)
    user_receiver = models.ForeignKey(UserProfile, related_name="user_receiver", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject

class Rating(models.Model):
    class RatingChoice(models.IntegerChoices):
        FIVE = 5
        FOUR = 4
        THREE = 3
        TWO = 2
        ONE = 1
        NONE = 0
    rating_receiver = models.ForeignKey(UserProfile, related_name="rating_receiver", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RatingChoice)
    comment = models.TextField()
    rating_sender = models.ForeignKey(UserProfile, related_name="rating_sender", on_delete=models.CASCADE)