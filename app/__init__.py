#FROM microblog/app/__init__.py
import logging
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import Config

from wtforms import *

from flask_migrate import Migrate

from flask_cors import CORS, cross_origin   #FOR THIS APP To TRANSFER FILES OVER DIFFERENT SERVERS


db = SQLAlchemy()

migrate = Migrate(compare_type=True)
bootstrap = Bootstrap()


#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/__init__.py	
def create_app(config_class=Config):
    
    app = Flask(__name__)
        
    app.config.from_object(config_class)
        
    db.init_app(app)    
    
    migrate.init_app(app, db)    
    bootstrap.init_app(app)
    
    from app.gts.gts import gt
    from app.select.select import slct    
    from app.task_manager.task_manager import tm
    from app.tasks.tasks import task
    
    app.register_blueprint(gt)    
    app.register_blueprint(slct)
    app.register_blueprint(tm)
    app.register_blueprint(task)

    return app

from app import models
from app.models import *
from app import *





