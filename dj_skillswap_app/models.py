from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"Skill: {self.name} in the category: {self.category}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} | {self.user.username}"

class Message(models.Model):
    user_sender = models.ForeignKey(Profile, related_name="user_sender", on_delete=models.CASCADE)
    user_receiver = models.ForeignKey(Profile, related_name="user_receiver", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject
    