
PYTHON = venv/bin/python
PIP = venv/bin/pip

venv:
	virtualenv venv;
	$(PIP) install -r ./requirements.txt

clear-venv:
	rm -rf ./venv

runserver: venv
	$(PYTHON) manage.py runserver

migrate: venv
	$(PYTHON) manage.py migrate

makemigrations: venv
	$(PYTHON) manage.py makemigrations

createsuperuser: venv
	$(PYTHON) manage.py createsuperuser

syncdb: venv
	$(PYTHON) manage.py syncdb
