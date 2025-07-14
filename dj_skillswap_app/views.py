from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import UserProfile


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
