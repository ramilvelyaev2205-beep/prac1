.PHONY: install run demo server test coverage lint

install:
	pip install -r requirements.txt

run:
	python -m src.repl

demo:
	python -m src.demo

server:
	python -m src.rpc_server

test:
	pytest -q

coverage:
	pytest --cov=src --cov-branch --cov-report=term-missing

lint:
	ruff check src tests
	radon cc src -s -a

