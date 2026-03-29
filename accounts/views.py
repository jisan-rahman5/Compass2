from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to COMPASS ✓')
            return redirect('dashboard:index')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
