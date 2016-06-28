from django import forms
from budget.models import Entry, Category
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class EntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(cat.id, cat) for cat in Category.objects.filter(user = user)]
        self.fields['value'].widget.attrs['step'] = 0.5

    class Meta:
        model = Entry
        fields = '__all__'
        exclude = ('user', )
        widgets = {'date': DateInput(),}

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        categories = Category.objects.filter(user = user)
        instance = kwargs.get('instance', None)
        if instance:
            categories = categories.exclude(id = instance.id)
        self.fields['parent'].choices = [(cat.id, cat) for cat in categories]

    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('user', )

