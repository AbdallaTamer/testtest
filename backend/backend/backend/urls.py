"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from users.views import signup_view
from databaseApi.views import profile_view
from users.views import signup_view,users,admins,coaches

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("",include('api.urls')),
    path('', signup_view, name='signup'),
    path("accouns/", include("allauth.urls")),
    path("main/", include("users.urls")),
    path("protected/",include("users.urls")),
    path('signup/', include('users.urls')),
    path('profile/', profile_view, name='profile/'),
    path('profilesData/',admins,name='profiles'),
    path('coachesData/',coaches,name='coaches'),
    path('usersData/',users,name='users'),
    path('profilesData/',admins,name='profiles'),
]
