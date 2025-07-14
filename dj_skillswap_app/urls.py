from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (register,edit_profile,view_profile,home,CustomLoginView) 

app_name = 'dj_skillswap_app'

urlpatterns = [
    path('',home, name='home'),
    path('signup/', register, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='dj_skillswap_app/logout.html'), name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/', view_profile, name='view_profile'),
]
