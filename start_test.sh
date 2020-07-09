export FLASK_ENV=Testing
#pytest -v --cov=blueprints tests/
pytest --cov-report html --cov=blueprints tests/
export FLASK_ENV=Development