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
    )


class Entry(models.Model):
    '''
    A journal entry
    '''
    # The category of the Entry
    category = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
    )

    # A string describing the entry
    label = models.CharField(
        max_length = settings.MAX_NAME_LENGTH,
        blank = False,
    )

    # A more detailed description of the category (not required)
    description = models.CharField(
        max_length = settings.MAX_DESCRIPTION_LENGTH,
    )

    # The date of the entry
    date = models.DateField(
        auto_now = True,
        blank = False,
    )

    # Is the expense essential (required but not considered when processing income)
    essential = models.BooleanField(
        default = False,
    )

    # Is the entry an expense or income
    is_expense = models.BooleanField(
        default = True,
    )

