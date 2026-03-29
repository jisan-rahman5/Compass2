from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    """A single task with date, priority, and completion status."""

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    PRIORITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    date = models.DateField(default=timezone.localdate)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # soft delete
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['completed', 'priority', '-created_at']

    def __str__(self):
        return self.title

    @property
    def priority_sort_key(self):
        return self.PRIORITY_ORDER.get(self.priority, 1)
