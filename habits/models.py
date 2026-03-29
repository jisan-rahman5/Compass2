from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    """A recurring daily habit that can be tracked as done/not done."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    """Daily log entry for a habit — binary done/not done."""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['habit']

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {'✓' if self.done else '✗'}"
