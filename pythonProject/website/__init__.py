from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, Resource, fields, marshal_with
import sqlite3, os
from flask import g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

db = SQLAlchemy()
current_directory = os.path.dirname(os.path.abspath(__file__))
if "home" not in current_directory:
    DB_NAME = "database.db"
"""
Initialize and configure the Flask app with necessary settings, blueprints, models, and resources.
Register endpoints for views and admin sections.
Create database tables if they do not exist.
Initialize and configure the LoginManager for user authentication.
Return the configured Flask app.
"""
def create_app():
    app = Flask(__name__)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    if "home" in current_directory:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://6186az:Sqlhaslo123@6186az.mysql.pythonanywhere-services.com/6186az$default'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = "secretkey4323423 23423"
    db.init_app(app)
    api=Api(app)

    from .views import views
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    from .models import Admin, Przepisy, Skladniki

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'views.index'
    login_manager.init_app(app)


    from .api import Dish_api, Ingredients_api


    api.add_resource(Dish_api, '/API/przepisy', '/API/przepisy/<input>')
    api.add_resource(Ingredients_api, '/API/skladniki', '/API/skladniki/<input>')

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app
