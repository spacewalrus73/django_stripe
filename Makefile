MANAGE := poetry run python3 manage.py

mkmig:
	@$(MANAGE) makemigrations

mig:
	@$(MANAGE) migrate

.PHONY: lint
lint:
	@poetry run flake8 product

.PHONY: port-clean
port-clean:
	sudo fuser -k 8000/tcp

.PHONY: run
run:
	docker run -p 8000:8000 djangostripe

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: build
build:
	docker build -t djangostripe .

runpy:
	@$(MANAGE) runserver
