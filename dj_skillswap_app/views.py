from django.shortcuts import render
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
                  Q(skill__category__icontains=param))
        posts = ProfileSkill.objects.filter(query)
    else:
        posts = ProfileSkill.objects.all()

    fields = [
        field for field in ProfileSkill._meta.fields
        if field.name not in EXCLUDED_FIELDS
    ]
    rows = []
    for post in posts:
        row = []
        for field in fields:
            # value = field.value_from_object(post)
            value = getattr(post, field.name)
            if field.is_relation and hasattr(value, 'pk'):
                value = str(value)
            row.append(value)
        rows.append(row)
    return render(request, 'dj_skillswap_app/browse_posts.html', context={'rows': rows,
                                                                          'fields': fields, })
