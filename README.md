# budgie
A Django based Expense tracker.


To run budgie.

git clone ...
cd ...
make venv
make migrate
make createsuperuser
Optionally create more users from the admin interface with the superuser login
make import_from_csv # Optional if you wish to import data from a csv, you will need to modify the script slightly
make runserver
