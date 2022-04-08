from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_, name='logout'),
]