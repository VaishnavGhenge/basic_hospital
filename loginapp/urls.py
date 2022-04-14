from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-post/edit/<str:val>/<int:id>/', views.save_post, name='postupdate'),
    path('post-delete/<int:id>/', views.delete_post, name='postdelete'),
    path('save-post/<str:val>/', views.save_post, name='postsave'),
    path('post/<int:id>/', views.postview, name='postview'),
    path('logout/', views.logout_, name='logout'),
]