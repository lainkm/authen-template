from django.urls import path
from . import views

urlpatterns = [
    path('github/', views.github_auth,name='github_oauth'),
    path('github_login/', views.githhub_login, name='github_login'),
]