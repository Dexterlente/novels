from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import app_config
from app.database import db
from app.routes import routes


def create_app():   
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(app_config)

    db.init_app(app)
    from app.models import novels
    from app.models import chapters
    migrate = Migrate(app, db)


    app.register_blueprint(routes)
    return app