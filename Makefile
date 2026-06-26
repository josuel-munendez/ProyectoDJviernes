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
PYTHON = python3
MANAGE = cd dcrm && ../$(VENV)/bin/python manage.py

setup: $(VENV)/bin/activate
	$(MANAGE) migrate --noinput
	$(MANAGE) seed_data

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -r requirements.txt --quiet
	touch $(VENV)/bin/activate

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test

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
