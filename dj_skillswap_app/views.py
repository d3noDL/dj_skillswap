from django.http import HttpResponseForbidden
from django.db.models import Q
from dj_skillswap_app.forms import AddProfileSkillForm, NewMessageForm, ReviewForm
from dj_skillswap_app.models import Category, Skill, UserProfileSkill, UserProfile, Message, Rating
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import JsonResponse
from faker import Faker
import random
from .utils import update_user_average_rating

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "✅ Your profile was updated successfully.")
            else:
                messages.info(request, "ℹ️ No changes detected.")
            return redirect('dj_skillswap_app:view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile/profile_edit.html', {'form': form})



@login_required
def view_profile(request):
    profile = request.user.userprofile
    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    user_posts = UserProfileSkill.objects.filter(profile=profile)
    reviews = Rating.objects.filter(rating_receiver=profile).order_by('-id')[:4]
    if selected_category:
        user_posts = user_posts.filter(skill__category_id=selected_category)

    return render(request, 'profile/profile_view.html', {
        'profile': profile,
        'user_posts': user_posts,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
        'reviews': reviews
    })




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('dj_skillswap_app:edit_profile')
    else:
        form = UserRegisterForm()
    return render(request, 'dj_skillswap_app/register.html', {'form': form})


def home(request):
    return render(request, 'core/home.html')


class CustomLoginView(LoginView):
    template_name = 'dj_skillswap_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        if not hasattr(profile, 'is_complete') or not profile.is_complete():
            return reverse('dj_skillswap_app:edit_profile')
        return reverse('dj_skillswap_app:view_profile')


def get_skills(request):
    category_id = request.GET.get('category_id')
    skills = Skill.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(skills), safe=False)


def skill_search(request):
    if 'param' in request.GET:
        param = request.GET['param']
        query = Q(Q(name__icontains=param) | Q(category__icontains=param))
        skill_data = Skill.objects.filter(query)
    else:
        skill_data = Skill.objects.all()
    contex = {'skill_data': skill_data}
    return render(request, 'dj_skillswap_app/skill_search.html', contex)


@login_required
def post_create(request):
    skills = Skill.objects.all()
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if not profile.bio or not profile.firstname and profile.lastname:  # verify if fields needed are filled
        messages.info(
            request, "Complete seu perfil antes de adicionar habilidades.")
        # redirect to profile edit page
        return redirect('dj_skillswap_app:edit_profile')
    if request.method == "POST":
        skill_form = AddProfileSkillForm(data=request.POST, user=request.user)

        if skill_form.is_valid():
            skill = skill_form.save(commit=False)
            skill.profile = profile
            skill.save()
            # redirect to the list of posts
            return redirect('dj_skillswap_app:post_list')
        else:
            messages.error(
                request, "Error on saving skill. Please verify the form.")
            return redirect('dj_skillswap_app:post_create')
    else:
        skill_form = AddProfileSkillForm(user=request.user)
    return render(request, "dj_skillswap_app/create_update_post.html", {"post_form": skill_form, "skills": skills})


def post_list(request):
    EXCLUDED_FIELDS = ['id', 'created_at', 'updated_at', 'description']
    param = request.GET.get('param', '')
    category_id = request.GET.get('category', '')

    query = Q()
    if param:
        query &= Q(skill__name__icontains=param) | Q(
            skill__category__name__icontains=param) | Q(type__icontains=param)
    if category_id:
        query &= Q(skill__category_id=category_id)

    posts = UserProfileSkill.objects.filter(query)

    categories = Category.objects.all()
    fields = [
        field for field in UserProfileSkill._meta.fields
        if field.name not in EXCLUDED_FIELDS
    ]

    rows = []
    for post in posts:
        row = {
            'id': post.id,
            'values': []
        }
        for field in fields:
            value = getattr(post, field.name)
            if field.is_relation and hasattr(value, 'pk'):
                value = str(value)
            elif isinstance(value, bool):
                value = "Active" if value else "Inactive"
            row['values'].append(value)
        rows.append(row)

    return render(request, 'dj_skillswap_app/posts_list.html', context={
        'posts': posts,
        'categories': categories,
        'search_term': param,
        'selected_category': int(category_id) if category_id else None
    })


@login_required
def post_update(request, id):
    skill = get_object_or_404(UserProfileSkill, pk=id)

    if skill.profile.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = AddProfileSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('dj_skillswap_app:post_list')
        else:
            messages.error(
                request, "Error updating post. Please verify the form.")
    else:
        form = AddProfileSkillForm(instance=skill)
    return render(request, 'dj_skillswap_app/create_update_post.html', {'post_form': form, 'post_data': skill})


def post_detail(request, id):
    post = get_object_or_404(UserProfileSkill, pk=id)
    recent_reviews = Rating.objects.filter(rating_receiver=post.profile).order_by('-id')[:3]



    return render(request, 'dj_skillswap_app/post_details.html', context={
        'post_data': post,
        'post_type': post.get_type_display(),
        'post_what': "What am I offering?" if post.type == "Offer" else "What do I need?",
        "reviews": recent_reviews
    })


@login_required
def toggle_post_status(request, id):
    post = get_object_or_404(UserProfileSkill, id=id)

    if request.user != post.profile.user:
        messages.error(request, "You are not allowed to modify this post.")
        return redirect('dj_skillswap_app:post_list')

    post.status = not post.status
    post.save()
    messages.success(request, "Post deactivated successfully.")
    return redirect('dj_skillswap_app:post_list')

@login_required
def inbox(request, message_id=None):
    current_profile = get_object_or_404(UserProfile, user=request.user)
    messages = Message.objects.filter(user_receiver=current_profile).order_by('-sent_at')
    selected_message = None

    if message_id:
        selected_message = get_object_or_404(Message, pk=message_id, user_receiver=current_profile)
        if not selected_message.is_read:
            selected_message.is_read = True
            selected_message.save()

    return render(request, 'dj_skillswap_app/inbox.html', {
        'messages': messages,
        'selected_message': selected_message
    })

@login_required
def send_message(request, id):
    reciever_profile = get_object_or_404(UserProfile, id=id)
    current_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        message_form = NewMessageForm(data=request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user_sender = current_profile
            message.user_receiver = reciever_profile
            message.save()
            messages.success(request, "Review submitted successfully!")
            return redirect("dj_skillswap_app:inbox")
        else:
            messages.error(request, "It happend an error while sending your message.")
    else:
        message_form = NewMessageForm()
    
    return render(request,"dj_skillswap_app/send_message.html", {"message_form": message_form, "reciever_profile": reciever_profile})

@login_required
def send_review(request, id):
    reviewed_profile = get_object_or_404(UserProfile, id=id)
    current_profile = get_object_or_404(UserProfile, user=request.user)
    print(reviewed_profile.average_rating)
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.rating_sender = current_profile
            review.rating_receiver = reviewed_profile
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect("dj_skillswap_app:post_list")
        else:
            messages.error(request, "It happend an error while saving your review.")
    else:
        review_form = ReviewForm()
    
    return render(request, "dj_skillswap_app/send_review.html", {"review_form": review_form, "reviewed_profile": reviewed_profile})


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    fake_users = [UserProfile.objects.order_by("?")[0] for _ in range(5)]
    total_users = len(UserProfile.objects.all())

    fake_activities = []
    for _ in range(11):
        fake_user = UserProfile.objects.order_by("?")[0]
        activities = [" posted a skill!", " engaged in a skillswap!", f" got rated {random.randint(0, 6)} star/s!"]
        fake_activities.append(f"{fake_user.firstname} {fake_user.lastname} {random.choice(activities)}")
    return render(request, "dj_skillswap_app/dashboard.html", {"users": fake_users, "activities": fake_activities, "total_users": total_users})