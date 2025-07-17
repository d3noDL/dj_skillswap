from django.shortcuts import render
from dj_skillswap_app.models import Category, UserProfileSkill


def home(request):
    categories = Category.objects.all()
    posts = UserProfileSkill.objects.all().order_by('-created_at')[:4]  # Get the latest 5 skills
    total_posts = UserProfileSkill.objects.count()
    return render(request, 'core/home.html', {'categories': categories, 'posts': posts, 'total_posts': total_posts})
