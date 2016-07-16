from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now


class Category(models.Model):
    '''
    The expense or income category
    '''
    def __str__(self):
        return self.name

    # The category name (required)
    name = models.CharField(
        max_length = settings.MAX_NAME_LENGTH,
        blank = False,
    )

    # A more detailed description of the category (not required)
    description = models.CharField(
        max_length = settings.MAX_DESCRIPTION_LENGTH,
        blank = True,
    )

    parent = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )

    # Every entry is owned by a user
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )


class Entry(models.Model):
    '''
    A journal entry
    '''
    def __str__(self):
        return self.label

    # A string describing the entry
    label = models.CharField(
        max_length = settings.MAX_NAME_LENGTH,
        blank = False,
    )

    # The cost of the expense or the amount of income
    value = models.DecimalField(
        blank = False,
        default = 0.00,
        decimal_places = 2,
        max_digits = 20,
    )

    # The date of the entry
    date = models.DateField(
        blank = False,
    )

    # The date-time created, used for sorting
    date_created = models.DateTimeField(
        auto_now_add = True,
    )

    # Is the entry an expense or income
    INCOME = 'income'
    EXPENSE = 'expense'
    flow_type = models.CharField(
        choices = (
            (INCOME, 'Income'),
            (EXPENSE, 'Expense'),
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
        blank = True,
    )

    # Is the expense essential (required but not considered when processing income)
    essential = models.BooleanField(
        default = False,
    )

    # Every entry is owned by a user
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
