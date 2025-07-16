from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (get_skills, register, edit_profile,
                    view_profile, home, CustomLoginView, skill_search, post_create, post_list, post_detail, post_update, send_message, inbox, send_review, toggle_post_status)

app_name = 'dj_skillswap_app'

urlpatterns = [
    path('signup/', register, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='dj_skillswap_app/logout.html'), name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/', view_profile, name='view_profile'),
    path('skills/search/', skill_search, name='skill_search'),
    path('posts/add/', post_create, name='post_create'),
    path('posts/', post_list, name='post_list'),
    path('post_details/<int:id>/', post_detail, name='post_details'),
    path('posts/<int:id>/edit/', post_update, name='post_update'),
    path('get-skills/', get_skills, name='get_skills'),
    path('post/<int:id>/toggle-status/', toggle_post_status, name='toggle_post_status'),
    path('inbox/', inbox, name="inbox"),
    path('send_message/', send_message, name="send_message"),
    path('send_review/', send_review, name="send_review"),
   
]
