# Makefile

.PHONY: install run

install:
	pip install -r requirements.txt

run:
	FLASK_APP=backend FLASK_ENV=development FLASK_DEBUG=1 flask run