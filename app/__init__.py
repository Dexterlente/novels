from flask import Flask
from config import app_config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(app_config)

from app.routes import routes
app.register_blueprint(routes)