from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from dj_skillswap_app.models import Skill, UserProfileSkill, UserProfile
from dj_skillswap_app.forms import AddProfileSkillForm
from django.db.models import Q
from django.contrib import messages


# Create your views here.


def search_skill(request):
    if 'param' in request.GET:
        param = request.GET['param']
        query = Q(Q(name__icontains=param) | Q(category__icontains=param))
        skill_data = Skill.objects.filter(query)
    else:
        skill_data = Skill.objects.all()
    contex = {'skill_data': skill_data}
    return render(request, 'dj_skillswap_app/browse_skill.html', contex)

# uncomment when we add authentication
# @login_required


def add_skill(request):
    skills = Skill.objects.all()
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if not profile.bio or not profile.firstname and profile.lastname:  # verify if fields needed are filled
        messages.info(
            request, "Complete seu perfil antes de adicionar habilidades.")
        return redirect('edit_profile')  # redirect to profile edit page
    if request.method == "POST":
        skill_form = AddProfileSkillForm(data=request.POST)

        if skill_form.is_valid():
            skill = skill_form.save()
            skill = skill_form.save(commit=False)
            skill.profile = profile
            skill.save()
            return redirect('posts')  # redirect to the list of posts
        else:
            messages.error(
                request, "Error on saving skill. Please verify the form.")
            return redirect('add_skill')
    else:
        skill_form = AddProfileSkillForm()

    return render(request, "dj_skillswap_app/add_profile_skill.html", {"add_skill_form": AddProfileSkillForm, "skills": skills})


def list_posts(request):
    EXCLUDED_FIELDS = ['id', 'created_at', 'updated_at', 'description']
    if 'param' in request.GET:
        param = request.GET['param']
        query = Q(Q(skill__name__icontains=param) |
                  Q(skill__category__icontains=param) |
                  Q(type__icontains=param))
        posts = UserProfileSkill.objects.filter(query)
    else:
        posts = UserProfileSkill.objects.all()

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
            row['values'].append(value)
        rows.append(row)
    return render(request, 'dj_skillswap_app/browse_posts.html', context={'rows': rows,
                                                                          'fields': fields, })


def edit_skill(request, id):
    skill = get_object_or_404(UserProfileSkill, pk=id)

    if skill.profile.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this skill.")

    if request.method == 'POST':
        form = AddProfileSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully.")
            return redirect('posts')
        else:
            messages.error(
                request, "Error updating skill. Please verify the form.")
    else:
        form = AddProfileSkillForm(instance=skill)
    return render(request, 'dj_skillswap_app/add_profile_skill.html', {'add_skill_form': form, 'post_data': skill})


def post_detail(request, id):
    post = get_object_or_404(UserProfileSkill, pk=id)
    fields = [field for field in UserProfileSkill._meta.fields if field.name not in [
        'created_at', 'updated_at']]

    post_data = {}
    for field in fields:
        value = getattr(post, field.name)
        value = str(value)
        post_data[field.verbose_name.title()] = value
        if post.type == 'Offer':
            post_type = "I'm offering "
            post_what = "What am I offering?"
        else:
            post_type = "I'm requesting "
            post_what = "What am I resquesting?"
    return render(request, 'dj_skillswap_app/post_details.html', context={'post_data': post, "post_type": post_type, "post_what": post_what})
