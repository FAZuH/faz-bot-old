.PHONY: build
build:
	docker-compose -f ./docker-compose.yml up --detach --build

.PHONY: up
up:
	docker-compose -f ./docker-compose.yml up --detach

.PHONY: down
down:
	docker-compose -f ./docker-compose.yml down


.PHONY: run
run:
	source .venv/bin/activate
	python -m fazbot

.PHONY: install
install:
	python3.12 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	cp .env-example .env

.PHONY: lint
lint:
	pylint fazbot\ --disable=R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,W
