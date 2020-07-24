from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models  # noqa: E402

# bottom import to deal with circular imports, common problem with Flask apps
# routes module must import the app variable from line 3
# put one the reciprocal imports at the bottom to avoid mutual references error
