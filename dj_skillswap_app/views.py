from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm

@login_required
def edit_profile(request):
    profile = request.user.userprofile  

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')  
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})

def view_profile(request):
    profile = request.user.userprofile
    return render(request, 'profile_view.html', {'profile': profile})

def home(request):
    return render(request, 'home.html')