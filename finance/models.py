from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Income(models.Model):
    """Monthly income entry."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=255)
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()

    class Meta:
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.source}: {self.amount} ({self.month}/{self.year})"


class Expense(models.Model):
    """Daily expense entry with category."""
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('shopping', 'Shopping'),
        ('bills', 'Bills & Utilities'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField(default=timezone.localdate)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.get_category_display()}: {self.amount} on {self.date}"
