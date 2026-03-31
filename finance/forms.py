from django import forms
from .models import Income, Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply the style.css form-control class to all fields automatically
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class IncomeForm(forms.ModelForm):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    month = forms.ChoiceField(choices=MONTH_CHOICES)

    class Meta:
        model = Income
        fields = ['amount', 'source', 'month', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
