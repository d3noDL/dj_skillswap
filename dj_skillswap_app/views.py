from django.shortcuts import render
from dj_skillswap_app.models import Skill
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

#uncomment when we add authentication
#@login_required
def add_skill(request):
    skills = Skill.objects.all()
    if request.method == "POST":
        skill_form = AddSkillForm(data=request.POST)

        if skill_form.is_valid():
            skill = skill_form.save()
            skill.save()
    else:
        skill_form = AddSkillForm()

    return render(request, "add_skill.html", {"add_skill_form": AddSkillForm, "skills": skills})
