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

def get_parent_choices_list(instance, user):
    categories = Category.objects.filter(user = user)
    if instance:
        categories = categories.exclude(id = instance.id)
    return [("", "--")] + [(cat.id, cat) for cat in categories]

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].choices = get_parent_choices_list(kwargs.get('instance', None), user)

    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('user', )

