import os
import django
import random
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_skillswap.settings")
django.setup()

from dj_skillswap_app.models import Category, Skill, UserProfile, UserProfileSkill, Rating, Message
from django.contrib.auth.models import User

faker = Faker()

def add_categories(n=5):
    for _ in range(n):
        name = faker.word()
        Category.objects.get_or_create(name=name)

def add_skills(n=7):
    categories = list(Category.objects.all())
    if not categories:
        print("No categories found. Run add_categories() first.")
        return

    for _ in range(n):
        name = faker.job()
        category = random.choice(categories)
        Skill.objects.get_or_create(name=name, category=category)

def add_users(n=150):
    for _ in range(n):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.unique.email()

        user_obj, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        UserProfile.objects.get_or_create(
            user=user_obj,
            defaults={
                "firstname": first_name,
                "lastname": last_name,
                "bio": faker.text(max_nb_chars=255),
                "profile_picture": faker.image_url(),
                "picture": faker.image_url(),
            }
        )

def add_skills_to_profiles(n=3):
    skills = list(Skill.objects.all())
    if not skills:
        print("No skills found. Run add_skills() first.")
        return

    for profile in UserProfile.objects.all():
        selected_skills = random.sample(skills, min(n, len(skills)))
        for skill in selected_skills:
            UserProfileSkill.objects.get_or_create(
                profile=profile,
                skill=skill,
                defaults={
                    "description": faker.text(max_nb_chars=255),
                    "type": random.choice(["Offer", "Request"]),
                    "avaliability": faker.text(max_nb_chars=64),
                    "pitch": faker.text(max_nb_chars=255),
                    "created_at": faker.date_time_this_year(),
                    "updated_at": faker.date_time_this_year(),
                    "status": faker.boolean(),
                }
            )

def add_ratings_to_profiles(n=None):
    profiles = list(UserProfile.objects.all())
    if len(profiles) < 2:
        print("Not enough user profiles to create ratings.")
        return

    for sender in profiles:
        num_ratings = n if n is not None else random.randint(1, 8)
        receivers = [p for p in profiles if p != sender]
        if not receivers:
            continue
        selected_receivers = random.sample(receivers, min(num_ratings, len(receivers)))
        for receiver in selected_receivers:
            Rating.objects.get_or_create(
                rating_sender=sender,
                rating_receiver=receiver,
                defaults={
                    "rating": random.randint(1, 5),
                    "comment": faker.text(max_nb_chars=255),
                }
            )

def add_messages(n=None):
    profiles = list(UserProfile.objects.all())
    if len(profiles) < 2:
        print("Not enough user profiles to send messages.")
        return

    num_messages = n if n is not None else random.randint(1, 15)

    for _ in range(num_messages):
        sender = random.choice(profiles)
        receivers = [p for p in profiles if p != sender]
        if not receivers:
            continue
        receiver = random.choice(receivers)
        Message.objects.get_or_create(
            user_sender=sender,
            user_receiver=receiver,
            defaults={
                "subject": faker.text(max_nb_chars=50),
                "message": faker.text(max_nb_chars=255),
            }
        )

if __name__ == "__main__":
    print("Adding categories...")
    add_categories()
    print("Adding skills...")
    add_skills()
    print("Adding users and user profiles...")
    add_users()
    print("Adding skills to user profiles...")
    add_skills_to_profiles()
    print("Adding ratings to user profiles...")
    add_ratings_to_profiles()
    print("Adding messages...")
    add_messages()
    print("Done!")
