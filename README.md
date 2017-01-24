# budgie
A Django based Expense tracker.

Uses entry of day to day expenses to provide high level summaries of spending patterns.

### Getting Started

Must have python3 and pip for python3 installed
```
apt-get python3 python3-pip
```

### Setup Virtualenv and Database
```
sudo pip install virtualenv
git clone https://github.com/Prodge/budgie.git; cd budgie
make venv
make migrate
make createsuperuser
```
Optionally create more users from the admin interface with the superuser login (localhost:8000/admin)

### Run the server
```
# Listen on localhost
make runserver

# Listen on all interfaces
make prodserver
```

### Import your own tracking from csv
If you wish to import data from a csv a script and make target are provided.

You will need to modify the script slightly.
The input csv file is defined in the script which can be found in:
```
/scripts/import_from_csv.py
```

Run the following make target when you are ready to import.
```
make import_from_csv
```
