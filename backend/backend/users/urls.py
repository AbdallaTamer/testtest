from django.urls import path,include
from . import views
from databaseApi.views import signup, login
from databaseApi.views import profile_view
from databaseApi.views import signup,get_Users,get_Profiles
from users.views import signup_view,users,admins,coaches

urlpatterns = [path('login/', views.login, name='login'),
                path('logout/', views.logout_view, name='logout'),
                path("protectedpage/",views.protected_page),
                path("test/",views.home),
                path('form/', views.form_view),
                path('signup/',views.signup),
                path('signupform/',signup, name = 'signupform'),
                path('loginform/',login, name = 'loginform'),
                path('users/',get_Users),
                path('admin/',get_Profiles),
                path('coaches/',get_Users),
                path('profilesData/',admins,name='profiles'),
                ]
