# budgie
A Django based Expense tracker.


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

### Import your own tracking from csv
Optional if you wish to import data from a csv.
You will need to modify the script slightly.
The input file is defined in the script.
The script can be found in /scripts/import_from_csv.py
```
make import_from_csv
```

### Run the server.
```
# Listen on localhost
make runserver

# Listen on all interfaces
make prodserver
```
