from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# bottom import to deal with circular imports, common problem with Flask apps
# routes module must import the app variable from line 3
# put one the reciprocal imports at the bottom to avoid mutual references error
