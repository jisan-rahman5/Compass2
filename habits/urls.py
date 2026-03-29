from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.habit_daily, name='daily'),
    path('manage/', views.habit_manage, name='manage'),
    path('add/', views.habit_create, name='create'),
    path('<int:pk>/edit/', views.habit_edit, name='edit'),
    path('<int:pk>/toggle/', views.habit_toggle, name='toggle'),
    path('<int:pk>/toggle-active/', views.habit_toggle_active, name='toggle_active'),
]
