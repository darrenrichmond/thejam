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
#this was not in the falsk mega tutorial, but wa necessary to get site working
#https://stackoverflow.com/questions/39908552/flask-loginexception-no-user-loader-has-been-installed-for-this-loginmanager
login.init_app(app)

from app import routes, models

#TODO: Add error logging 
#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling