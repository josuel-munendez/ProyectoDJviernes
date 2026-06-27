.PHONY: help setup run test docker docker-build clean

help:
	@echo "Uso: make <comando>"
	@echo ""
	@echo "Comandos:"
	@echo "  setup        Crear entorno virtual, instalar dependencias, migrar y seed"
	@echo "  run          Iniciar servidor de desarrollo"
	@echo "  test         Ejecutar tests"
	@echo "  docker       Iniciar con Docker Compose"
	@echo "  docker-build Construir imágenes Docker"
	@echo "  clean        Eliminar entorno virtual y archivos temporales"

VENV = entorno
MANAGE = python manage.py
UNAME := $(shell uname -s)

ifeq ($(OS),Windows_NT)
PYTHON = python
ACTIVATE = $(VENV)\Scripts\activate.bat
RUN_IN_VENV = $(ACTIVATE) && pip install -r requirements.txt --quiet && $(MANAGE)
else
PYTHON = python3
ACTIVATE = $(VENV)/bin/activate
RUN_IN_VENV = . $(ACTIVATE) && pip install -r requirements.txt --quiet && $(MANAGE)
endif

setup: $(ACTIVATE)
	cd dcrm && bash -c "$(RUN_IN_VENV) migrate --noinput && $(RUN_IN_VENV) seed_data"

$(ACTIVATE): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(RUN_IN_VENV) collectstatic --noinput 2>/dev/null || true
	touch $(ACTIVATE)

run:
	cd dcrm && $(PYTHON) manage.py runserver

test:
	cd dcrm && $(PYTHON) manage.py test

docker:
	docker compose up -d
	@echo "Abrir http://localhost:8000"

docker-build:
	docker compose build

clean:
	rm -rf $(VENV)
	rm -rf dcrm/staticfiles
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "Limpieza completada"
