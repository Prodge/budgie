
PYTHON = venv/bin/python3
PIP = venv/bin/pip3

venv:
	virtualenv -p /usr/bin/python3 venv;
	$(PIP) install -r ./requirements.txt

clear_venv:
	rm -rf ./venv

runserver: venv
	$(PYTHON) manage.py runserver_plus

prodserver: venv
	$(PYTHON) manage.py runserver 0.0.0.0:8000

shell: venv
	$(PYTHON) manage.py shell_plus

migrate: venv
	$(PYTHON) manage.py migrate

makemigrations: venv
	$(PYTHON) manage.py makemigrations

createsuperuser: venv
	$(PYTHON) manage.py createsuperuser

import_from_csv: venv
	$(PYTHON) manage.py runscript import_from_csv
