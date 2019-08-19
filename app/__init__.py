from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from Config import Config



app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


