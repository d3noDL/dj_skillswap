from django.shortcuts import get_object_or_404, render
from dj_skillswap_app.models import Skill, ProfileSkill
from dj_skillswap_app.forms import AddProfileSkillForm
from django.db.models import Q

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
    if request.method == "POST":
        skill_form = AddProfileSkillForm(data=request.POST)

        if skill_form.is_valid():
            skill = skill_form.save()
            skill.save()
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
        posts = ProfileSkill.objects.filter(query)
    else:
        posts = ProfileSkill.objects.all()

    fields = [
        field for field in ProfileSkill._meta.fields
        if field.name not in EXCLUDED_FIELDS
    ]
    rows = []
    for post in posts:
        row = {
            'id': post.id,  # Mantém o ID separado (para links)
            'values': []
        }
        for field in fields:
            # value = field.value_from_object(post)
            value = getattr(post, field.name)
            if field.is_relation and hasattr(value, 'pk'):
                value = str(value)
            row['values'].append(value)
        rows.append(row)
    return render(request, 'dj_skillswap_app/browse_posts.html', context={'rows': rows,
                                                                          'fields': fields, })


def post_detail(request, id):
    post = get_object_or_404(ProfileSkill, pk=id)
    fields = [field for field in ProfileSkill._meta.fields if field.name not in [
        'id', 'created_at', 'updated_at']]

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
