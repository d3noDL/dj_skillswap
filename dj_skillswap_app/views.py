from django.shortcuts import render
from dj_skillswap_app.forms import AddSkillForm
from dj_skillswap_app.models import Skill

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
