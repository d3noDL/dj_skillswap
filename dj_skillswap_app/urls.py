from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dj_skillswap_app'

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='dj_skillswap_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='dj_skillswap_app/logout.html'), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
]
