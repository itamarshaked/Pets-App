import os
import time

from flask import Flask
from sqlalchemy import create_engine

from app.extensions import db, jwt
from app.pets.routes import pets_bp
from app.auth.routes import auth_bp


def wait_for_db(database_url):
    for i in range(10):
        try:
            engine = create_engine(database_url)
            connection = engine.connect()
            connection.close()
            print("Database connected!")
            return
        except Exception:
            print("Database not ready yet...")
            time.sleep(2)

    raise Exception("Database connection failed")


def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")

    wait_for_db(database_url)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "dev-secret-key"
    )

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(pets_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app