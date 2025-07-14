"""
URL configuration for dj_skillswap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dj_skillswap_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('skills/', views.search_skill, name='search_skill'),
    path('add_skill/', views.add_skill, name="add_skill"),
    path('browse_posts/', views.list_posts, name="posts"),
    path('post_details/<int:id>/', views.post_detail, name='post_details'),
    path('edit_post/<int:id>/', views.edit_skill, name='edit_post')
]
