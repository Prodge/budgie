#
# Import expense entries from a csv sheet.
# This may need to be modified for your own use.
#
# First argument is file name (csv)
#

import csv
import datetime

from django.contrib.auth.models import User

from budget.models import Category, Entry


#Document formatting
delimiter_character = ','
text_delimiter_character = '"'

columns = {
    'date': 1,
    'category': 2,
    'label': 3,
    'essential': 4,
    'amount': 5,
}

def get_input_document(input_document_name):
    '''
    Takes a filename as an input and returns a 2D array of the csv
    '''
    with open(input_document_name, 'rb') as input_file:
        input_document_reader = csv.reader(
            input_file,
            delimiter = delimiter_character,
            quotechar = text_delimiter_character
        )
        return [row for row in input_document_reader]

def get_user():
    '''
    The user to assign all of the categories and entries to
    '''
    return User.objects.latest('id')

def create_categories(categories):
    '''
    Creates category objects given a list of category name strings
    '''
    for category in categories:
        category = Category.get_or_create(name = category, user = get_user())
        category.save()

def create_entries(entries):
    '''
    Creates entry objects given the csv data where each row is an entry
    '''
    for entry in entries:
        flow_type = 'income' if entry[columns['category']] == 'Income' else 'expense'
        essential = entry[columns['essential']] == 'y'
        entry = Entry(
            label = entry[columns['label']],
            value = entry[columns['amount']],
            date = datetime.datetime.strptime(entry[columns['date']], "%d/%m/%Y").date(),
            flow_type = flow_type,
            category = Category.objects.get(name = entry[columns['category']]),
            essential = essential,
            user = get_user()
        )
        entry.save()

def main():
    input_csv = '~/downloads/journal.csv'
    entries = input_csv[4:]
    create_categories([entry[columns['category']] for entry in entries])
    create_entries(entries)

main()
