"""COMPASS URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard:index')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('tasks/', include('tasks.urls')),
    path('habits/', include('habits.urls')),
    path('finance/', include('finance.urls')),
]
