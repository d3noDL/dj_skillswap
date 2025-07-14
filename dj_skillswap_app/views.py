from django.http import HttpResponseForbidden
from django.db.models import Q
from dj_skillswap_app.forms import AddProfileSkillForm
from dj_skillswap_app.models import Category, Skill, UserProfileSkill, UserProfile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import JsonResponse


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dj_skillswap_app:view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile/profile_edit.html', {'form': form})


@login_required
def view_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile/profile_view.html', {'profile': profile})


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
        'rows': rows,
        'fields': fields,
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

    if post.type == 'Offer':
        post_type = "I'm offering "
        post_what = "What am I offering?"
    else:
        post_type = "I'm requesting "
        post_what = "What am I requesting?"

    return render(request, 'dj_skillswap_app/post_details.html', context={
        'post_data': post,
        'post_type': post_type,
        'post_what': post_what,
    })
