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
git clone ...
cd ...
make venv
make migrate
make createsuperuser
# Optionally create more users from the admin interface with the superuser login

# Optional if you wish to import data from a csv, you will need to modify the script slightly
make import_from_csv
```

### Run the server.
```
# Listen on localhost
make runserver

# Listen on all interfaces
make prodserver
```
