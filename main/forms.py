from django import forms
from .models import Todo
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class TodoForm(forms.ModelForm):
    deadline = forms.DateField(widget=DatePicker())

    class Meta():
        model = Todo
        fields = ('text', 'category')


