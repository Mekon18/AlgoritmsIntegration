"""
Definition of urls for AlgoritmsIntegration.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('bees/', views.bees, name='bees'),
    path('fishes/', views.fishes, name='fishes'),
    path('fireflies/', views.fireflies, name='fireflies'),
    path('wait/', views.wait, name='wait'),
    path('result/', views.result, name='result'),
    path('result/animation', views.animation, name='animation'),
    path('init/', views.init, name='init'),
    path('ants/', views.ants, name='ants'),
    path('getNextMove/', views.getNextMove, name='getNextMove'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
