from budget.models import Category

def show_num_category_entries(categories):
    for cat in categories:
        print('"{}" has {} entries'.format(cat.name, cat.entry_set.count()))

def combine_categories(cat1, cat2):
    show_num_category_entries([cat1, cat2])

    print('Moving "{}" entries to "{}"'.format(cat1.name, cat2.name))
    for entry in cat1.entry_set.all():
        entry.category = cat2
        entry.save()

    show_num_category_entries([cat1, cat2])

    print('Removing "{}"'.format(cat1.name))
    cat1.delete()

def combine_categories_by_id(id1, id2):
    combine_categories(
        Category.objects.get(id = id1),
        Category.objects.get(id = id2)
    )
