from django.db import models


class Category(models.Model):
    '''
    The expense category
    '''


class Entry(models.Model):
    '''
    A journal entry
    '''
    category = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
    )

    # A string describing the entry
    label = models.CharField(
        max_length = 200,
    )

    # The date of the entry
    date = models.DateField(
        auto_now = True,
    )

    # Is the expense essential (required but not considered when processing income)
    essential = models.BooleanField(
        default = False,
    )

    # Is the entry an expense or income
    is_expense = models.BooleanField(
        default = True,
    )

