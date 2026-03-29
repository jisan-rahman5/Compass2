from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, date
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    """List tasks for a specific date (default: today)."""
    date_str = request.GET.get('date')
    if date_str:
        try:
            view_date = date.fromisoformat(date_str)
        except ValueError:
            view_date = timezone.localdate()
    else:
        view_date = timezone.localdate()

    today = timezone.localdate()
    is_future = view_date > today
    prev_date = view_date - timedelta(days=1)
    next_date = view_date + timedelta(days=1)

    tasks = (
        Task.objects
        .filter(user=request.user, date=view_date, is_deleted=False)
        .order_by('completed', 'priority', '-created_at')
    )

    # Sort by priority order: high=0, medium=1, low=2
    tasks = sorted(tasks, key=lambda t: (t.completed, t.priority_sort_key))

    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'view_date': view_date,
        'today': today,
        'is_future': is_future,
        'prev_date': prev_date,
        'next_date': next_date,
    })


@login_required
def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added ✓')
            return redirect(f'/tasks/?date={task.date.isoformat()}')
    else:
        initial_date = request.GET.get('date', timezone.localdate().isoformat())
        form = TaskForm(initial={'date': initial_date})

    return render(request, 'tasks/form.html', {'form': form, 'action': 'Add'})


@login_required
def task_edit(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk, user=request.user, is_deleted=False)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save()
            messages.success(request, 'Task updated ✓')
            return redirect(f'/tasks/?date={updated_task.date.isoformat()}')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/form.html', {'form': form, 'action': 'Edit'})


@login_required
def task_delete(request, pk):
    """Soft-delete a task."""
    task = get_object_or_404(Task, pk=pk, user=request.user, is_deleted=False)
    if request.method == 'POST':
        task.is_deleted = True
        task.save()
        messages.success(request, 'Task removed ✓')
    return redirect(f'/tasks/?date={task.date.isoformat()}')


@login_required
def task_toggle(request, pk):
    """Toggle task completion."""
    task = get_object_or_404(Task, pk=pk, user=request.user, is_deleted=False)

    if request.method == 'POST':
        task.completed = not task.completed
        task.save()

    referer = request.META.get('HTTP_REFERER')
    if referer and 'dashboard' in referer:
        return redirect('dashboard:index')
    return redirect(f'/tasks/?date={task.date.isoformat()}')
