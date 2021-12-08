web: gunicorn run:app --log-level=debug

init: python db_create.py
migrate: python db_migrate.py
upgrade: python db_upgrade.py
