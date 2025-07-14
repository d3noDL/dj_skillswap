from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
<<<<<<< HEAD
from .forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm
=======
from .forms import UserProfileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login

>>>>>>> b1b29b516536ce54bd2be856ac7cd4dba61402dd

@login_required
def edit_profile(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)

<<<<<<< HEAD
    return render(request, 'profile/profile_edit.html', {'form': form})
=======
    return render(request, 'profile_edit.html', {'form': form})

>>>>>>> b1b29b516536ce54bd2be856ac7cd4dba61402dd
@login_required
def view_profile(request):
    profile = request.user.userprofile
    return render(request, 'profile/profile_view.html', {'profile': profile})

<<<<<<< HEAD
def home(request):
    return render(request, 'home.html')
=======
>>>>>>> b1b29b516536ce54bd2be856ac7cd4dba61402dd

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


<<<<<<< HEAD
=======
def home(request):
    return render(request, 'core/home.html')
>>>>>>> b1b29b516536ce54bd2be856ac7cd4dba61402dd
