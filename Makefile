# Python + Flask makefile

VENV = .venv
VENV_PYTHON3 = $(VENV)/bin/python3

all: venv deps

venv: $(VENV_PYTHON3)
$(VENV_PYTHON3):
	python3 -m venv "$(VENV)"

deps: venv
	$(VENV_PYTHON3) -m pip install -r requirements.txt

run:
	$(VENV_PYTHON3) server.py

zip:
	rm -f archive.zip
	zip -r archive.zip . -x '.venv/*' -x '*__pycache__/*' -x '*.zip' -x '*.db'

