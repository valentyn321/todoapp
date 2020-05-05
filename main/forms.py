from django import forms
from .models import Todo
from django.utils import timezone
from tempus_dominus.widgets import DatePicker


class TodoForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=DatePicker(
            options={
                'minDate': timezone.now().strftime("%Y-%m-%d"),
            },
        ),
        initial=timezone.now().strftime("%Y-%m-%d"),
    )

    class Meta():
        model = Todo
        fields = ('text', 'category')


