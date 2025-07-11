from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login


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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/')  # Redirect to the home page or another page
    else:
        form = UserRegisterForm()
    return render(request, 'dj_skillswap_app/register.html', {'form': form})


def home(request):
    return render(request, 'core/home.html')
