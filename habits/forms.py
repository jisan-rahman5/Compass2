from django import forms
from .models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Read for 20 minutes',
            }),
        }
