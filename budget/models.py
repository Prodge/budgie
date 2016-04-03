from django.db import models
from django.conf import settings


class Category(models.Model):
    '''
    The expense or income category
    '''
    # The category name (required)
    name = models.CharField(
        max_length = settings.MAX_NAME_LENGTH,
        blank = False,
    )

    # A more detailed description of the category (not required)
    description = models.CharField(
        max_length = settings.MAX_DESCRIPTION_LENGTH,
    )

    parent = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )


class Entry(models.Model):
    '''
    A journal entry
    '''
    # A string describing the entry
    label = models.CharField(
        max_length = settings.MAX_NAME_LENGTH,
        blank = False,
    )

    # The date of the entry
    date = models.DateField(
        auto_now = True,
        blank = False,
    )

    # Is the entry an expense or income
    flow_type = models.CharField(
        choices = (
            ('income', 'Income'),
            ('expense', 'Expense'),
        ),
        max_length = 50,
        default = 'expense',
    )

    # The category of the Entry (Required. User is encouraged to create an uncategorized category)
    category = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
    )

    # A more detailed description of the Entry (not required)
    description = models.CharField(
        max_length = settings.MAX_DESCRIPTION_LENGTH,
    )

    # Is the expense essential (required but not considered when processing income)
    essential = models.BooleanField(
        default = False,
    )

