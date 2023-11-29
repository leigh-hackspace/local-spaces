.venv:
	python3 -m pip install poetry
	python3 -m poetry install

serve:
	FLASK_DEBUG=1 FLASK_APP=local_spaces.app:create_app .venv/bin/flask run --reload --debug -p 5001

tests: .venv
	python3 -m poetry run pytest || true

lint: .venv
	python3 -m poetry run ruff --output-format=github --select=E9,F63,F7,F82 --target-version=py37 .
	python3 -m poetry run ruff --output-format=github --target-version=py37 .