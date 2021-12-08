from flask import Blueprint

from app import db
from app import models, task_manager


tm = Blueprint('tm', __name__, template_folder='templates')

from . import task_manager