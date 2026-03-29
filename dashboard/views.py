import calendar
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from tasks.models import Task
from habits.models import Habit, HabitLog
from finance.models import Income, Expense


@login_required
def dashboard_view(request):
    """Daily orientation screen with finance summary, tasks, habits, and notes."""
    today = timezone.localdate()
    user = request.user
    year = today.year
    month = today.month

    # --- Greeting ---
    greeting = f"Hey {user.username}"

    # --- Year Progress ---
    is_leap = calendar.isleap(year)
    total_days = 366 if is_leap else 365
    day_of_year = today.timetuple().tm_yday
    days_left = total_days - day_of_year
    pct_complete = round((day_of_year / total_days) * 100, 1)

    # --- Finance Summary (This Month) ---
    total_income = Income.objects.filter(
        user=user, month=month, year=year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    total_expense = Expense.objects.filter(
        user=user, date__month=month, date__year=year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    savings = total_income - total_expense

    month_name = [
        '', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ][month]

    # --- Calculations ---
    _, days_in_month = calendar.monthrange(year, month)
    days_left_month = days_in_month - today.day
    
    _savings = savings if savings > 0 else Decimal('0.00')
    total = total_income + total_expense + _savings
    if total > 0:
        income_pct = int((total_income / total) * 100)
        expense_pct = int((total_expense / total) * 100)
        savings_pct = int((_savings / total) * 100)
    else:
        income_pct, expense_pct, savings_pct = 0, 0, 100

    # --- Today's Focus (tasks) ---
    todays_tasks = (
        Task.objects.filter(user=user, date=today, is_deleted=False)
        .order_by('completed', 'priority')
    )
    todays_tasks = sorted(todays_tasks, key=lambda t: (t.completed, t.priority_sort_key))

    # --- Daily Anchors (habits list for today) ---
    active_habits = Habit.objects.filter(user=user, active=True)
    todays_habits = []
    for habit in active_habits:
        is_done = HabitLog.objects.filter(habit=habit, date=today, done=True).exists()
        todays_habits.append({
            'pk': habit.pk,
            'name': habit.name,
            'completed': is_done
        })

    # --- End ---

    return render(request, 'dashboard/index.html', {
        'greeting': greeting,
        'today': today,
        'year': year,
        'month_name': month_name,
        'total_days': total_days,
        'days_left': days_left,
        'day_of_year': day_of_year,
        'pct_complete': pct_complete,
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'todays_tasks': todays_tasks,
        'todays_habits': todays_habits,
        'days_left_month': days_left_month,
        'income_pct': income_pct,
        'expense_pct': expense_pct,
        'savings_pct': savings_pct,
    })
