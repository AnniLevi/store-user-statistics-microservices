from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    from .views import api_bp

    app.register_blueprint(api_bp)

    @app.route("/")
    def hello():
        return "Hello in User Personal Info - Flask"

    return app
