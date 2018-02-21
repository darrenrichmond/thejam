from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

#TODO: Add error logging 
#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling