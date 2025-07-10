from django.shortcuts import render
from dj_skillswap_app.forms import AddSkillForm, NewMessageForm
from dj_skillswap_app.models import Skill, Message, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

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
            print(skill_form.errors)
    else:
        skill_form = AddSkillForm()

    return render(request, "add_skill.html", {"add_skill_form": AddSkillForm, "skills": skills})

#uncomment when we add authentication
#@login_required
def inbox(request):
    #Change this view so it's just for the logged in user
    messages = Message.objects.all()
    return render(request, "inbox.html", {"messages": messages})

#uncomment when we add authentication
#@login_required
def send_message(request):
    if request.method == "POST":
        message_form = NewMessageForm(data=request.POST)

        if message_form.is_valid():
            current_profile = get_object_or_404(Profile, user=request.user)
            message = message_form.save(commit=False)
            message.user_sender = current_profile
            message.save()
            return HttpResponseRedirect(reverse("inbox"))
        else:
            print(message_form.errors)
    else:
        message_form = NewMessageForm()
    
    return render(request,"send_message.html", {"message_form": message_form})