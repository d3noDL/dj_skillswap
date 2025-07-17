from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Rating
from .utils import update_user_average_rating

@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, "userprofile"):
            instance.userprofile.save()


@receiver(post_save, sender=Rating)
def update_average_rating_on_review(sender, instance, **kwargs):
    update_user_average_rating(instance.rating_receiver)