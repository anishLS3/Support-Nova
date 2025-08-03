from flask import Flask
from config import Config
from flask_cors import CORS

from database.complaint_db import init_db  

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    init_db()
    from main.routes import main
    app.register_blueprint(main)

    return app
