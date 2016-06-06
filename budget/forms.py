from django import forms
from budget.models import Entry, Category
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class EntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(cat.id, cat) for cat in Category.objects.filter(user = user)]

    class Meta:
        model = Entry
        fields = '__all__'
        exclude = ('user', )
        widgets = {'date': DateInput(),}

