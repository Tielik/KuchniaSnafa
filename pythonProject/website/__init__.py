from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, Resource, fields, marshal_with
import sqlite3
from flask import g

db = SQLAlchemy()
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
    app.config['SECRET_KEY'] = "secretkey4323423 23423"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
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

    resource_fields={
         'id': fields.Integer,
         'nazwa': fields.String,
         'czas': fields.String,
         'opis': fields.String,
         'skladniki': fields.String,
         'przepis': fields.String,
     }
    resource_fields2 = {
        'id': fields.Integer,
        'Nazwa': fields.String,
        'kategoria': fields.Integer
    }
    class Dish_api(Resource):
        @marshal_with(resource_fields)
        def get(self):
            return Przepisy.query.all()

    class Ingredients_api(Resource):
        @marshal_with(resource_fields2)
        def get(self):
            return Skladniki.query.all()

    api.add_resource(Dish_api, '/API/przepisy')
    api.add_resource(Ingredients_api, '/API/skladniki')

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app
