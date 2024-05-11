from flask import Flask
from config import app_config
from app.views import views

app = Flask(__name__)
app.config.from_object(app_config)

app.register_blueprint(views)

