import csv
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Income, Expense
from .forms import ExpenseForm, IncomeForm


@login_required
def finance_overview(request):
    """Monthly finance overview with income, expenses, and savings."""
    today = timezone.localdate()

    try:
        month = int(request.GET.get('month', today.month))
        year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        month, year = today.month, today.year

    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    month_name = [
        '', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ][month]

    # Queries
    incomes = Income.objects.filter(user=request.user, month=month, year=year)
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=year)
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    savings = total_income - total_expense
    recent_expenses = expenses[:10]

    # Calculate percentage for purely native CSS bar chart
    if total_income > 0:
        expense_percentage = min(int((total_expense / total_income) * 100), 100)
    else:
        expense_percentage = 0 if total_expense == 0 else 100

    # Category breakdown for the pie chart
    from django.db.models import Sum as _Sum
    category_totals = (
        expenses.values('category')
        .annotate(total=_Sum('amount'))
        .order_by('-total')
    )
    cat_labels = []
    cat_values = []
    for ct in category_totals:
        # get the human-friendly label from choices
        label = dict(Expense.CATEGORY_CHOICES).get(ct['category'], ct['category'].title())
        cat_labels.append(label)
        cat_values.append(float(ct['total']))

    return render(request, 'finance/overview.html', {
        'month': month,
        'year': year,
        'month_name': month_name,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'incomes': incomes,
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'expense_percentage': expense_percentage,
        'recent_expenses': recent_expenses,
        'cat_labels': cat_labels,
        'cat_values': cat_values,
    })


@login_required
def expense_add(request):
    """Add a new expense."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added ✓')
            return redirect('finance:overview')
    else:
        form = ExpenseForm(initial={'date': timezone.localdate()})

    return render(request, 'finance/expense_form.html', {'form': form})


@login_required
def expense_edit(request, pk):
    """Edit an expense."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated ✓')
            return redirect('finance:overview')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'finance/expense_form.html', {'form': form, 'editing': True})


@login_required
def expense_delete(request, pk):
    """Delete an expense."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense removed ✓')
    return redirect('finance:overview')


@login_required
def income_manage(request, pk=None):
    """Add or edit income entries. If pk is provided, edit that entry."""
    today = timezone.localdate()

    if pk:
        income_obj = get_object_or_404(Income, pk=pk, user=request.user)
    else:
        income_obj = None

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income_obj)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            msg = 'Income updated ✓' if pk else 'Income added ✓'
            messages.success(request, msg)
            return redirect('finance:income')
    else:
        if income_obj:
            form = IncomeForm(instance=income_obj)
        else:
            form = IncomeForm(initial={'month': today.month, 'year': today.year})

    incomes = Income.objects.filter(user=request.user)
    return render(request, 'finance/income.html', {
        'form': form,
        'incomes': incomes,
        'editing': pk is not None,
    })


@login_required
def income_delete(request, pk):
    """Delete an income entry."""
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income removed ✓')
    return redirect('finance:income')


@login_required
def export_finances_csv(request):
    """Export the user's finances for the current month as a CSV."""
    today = timezone.localdate()
    month = today.month
    year = today.year

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="compass_finance_{year}_{month}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Type', 'Date', 'Category/Note', 'Amount'])

    # Write Incomes
    incomes = Income.objects.filter(user=request.user, month=month, year=year)
    for inc in incomes:
        writer.writerow(['Income', f'{year}-{month:02d}', 'Monthly Income', inc.amount])

    # Write Expenses
    expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=year).order_by('date')
    for exp in expenses:
        note = exp.note if exp.note else exp.get_category_display()
        writer.writerow(['Expense', exp.date, note, exp.amount])

    return response
