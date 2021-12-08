from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db

from app.models import General_txt

from app.forms import LoginForm, EditForm

from sqlalchemy import update

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
tm = Blueprint(
    'task_manager', __name__,
    template_folder='templates'
)
   
from app.gts.gts import edit_gts

#from app import *


@tm.route('/', methods=['GET', 'POST'])
@tm.route('/index', methods=['GET', 'POST'])
@tm.route('/edit_tms', methods=['GET', 'POST'])
def edit_tms():

    print("IN edit_tms")
    print("")
    
    return edit_gts()   