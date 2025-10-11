from django.urls import path
from . import provider_views

urlpatterns = [
    path('signup/', provider_views.provider_signup, name='provider_signup'),
    path('login/', provider_views.provider_login, name='provider_login'),
  #  path('logout/', provider_views.provider_logout, name='provider_logout'),
   # path('dashboard/', provider_views.provider_dashboard, name='provider_dashboard'),
    #path('profile/', provider_views.provider_profile, name='provider_profile'),
]