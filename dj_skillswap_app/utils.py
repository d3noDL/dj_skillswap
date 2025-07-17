from django.db.models import Avg
from .models import Rating, UserProfile

def update_user_average_rating(profile: UserProfile):
    average = Rating.objects.filter(rating_receiver=profile).aggregate(avg=Avg('rating'))['avg'] or 0
    profile.average_rating = round(average, 1)
    profile.save()