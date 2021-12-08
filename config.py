import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:postgres@localhost:5432/task_manager'
    
    #'postgresql://postgres:tomererezor1@localhost:5432/menta4_from_heroku'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tomererezor1@localhost:5432/menta'       #menta db   
    
    #SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    #SQLALCHAMY_ECHO = True

    
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    print("SQLALCHEMY_MIGRATE_REPO IS : ", SQLALCHEMY_MIGRATE_REPO)
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    
        
    
