from django import forms
from budget.models import Entry
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        widgets = {'date': DateInput(),}

