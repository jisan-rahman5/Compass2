from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Habit, HabitLog
from .forms import HabitForm


def _calculate_streak(habit, today):
    """Count how many consecutive days (going backward from today) this habit was done."""
    streak = 0
    check_date = today
    while True:
        done = HabitLog.objects.filter(habit=habit, date=check_date, done=True).exists()
        if done:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    return streak


@login_required
def habit_daily(request):
    """Daily habit checklist for today."""
    today = timezone.localdate()
    habits = Habit.objects.filter(user=request.user, active=True)

    # Ensure HabitLog entries exist for today and calculate streak
    habit_data = []
    for habit in habits:
        log, _ = HabitLog.objects.get_or_create(habit=habit, date=today)
        streak = _calculate_streak(habit, today)
        habit_data.append({'habit': habit, 'log': log, 'streak': streak})

    return render(request, 'habits/daily.html', {
        'habit_data': habit_data,
        'today': today,
    })


@login_required
def habit_toggle(request, pk):
    """Toggle a habit's done status for today."""
    habit = get_object_or_404(Habit, pk=pk, user=request.user, active=True)
    today = timezone.localdate()

    if request.method == 'POST':
        log, _ = HabitLog.objects.get_or_create(habit=habit, date=today)
        log.done = not log.done
        log.save()

    referer = request.META.get('HTTP_REFERER')
    if referer and 'dashboard' in referer:
        return redirect('dashboard:index')
    return redirect('habits:daily')


@login_required
def habit_manage(request):
    """List all habits for management."""
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/manage.html', {'habits': habits})


@login_required
def habit_create(request):
    """Create a new habit."""
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Habit added ✓')
            return redirect('habits:manage')
    else:
        form = HabitForm()

    return render(request, 'habits/form.html', {'form': form, 'action': 'Add'})


@login_required
def habit_edit(request, pk):
    """Edit a habit's name."""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habit updated ✓')
            return redirect('habits:manage')
    else:
        form = HabitForm(instance=habit)

    return render(request, 'habits/form.html', {'form': form, 'action': 'Edit'})


@login_required
def habit_toggle_active(request, pk):
    """Activate or deactivate a habit."""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        habit.active = not habit.active
        habit.save()
        status = 'activated' if habit.active else 'deactivated'
        messages.success(request, f'Habit {status} ✓')

    return redirect('habits:manage')
