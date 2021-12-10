#!/usr/bin/env python

pip install flask;

pip install flask_sqlalchemy;
pip install flask_wtf;
pip install psycopg2;
pip install  sqlalchemy-migrate;
pip install flask_migrate;
pip install gunicorn;
pip install psycopg2-binary;
pip install flask-bootstrap;

set FLASK_ENV=development;
set FLASK_APP=run.py;
set FLASK_RUN_PORT=5000
flask run
