from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline', 'is_completed']
