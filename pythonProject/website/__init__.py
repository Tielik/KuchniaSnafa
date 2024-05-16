from flask import Flask, request
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
         'ListaSkladnikow': fields.String,
         'przepis': fields.String,
     }
    resource_fields2 = {
        'id': fields.Integer,
        'Nazwa': fields.String,
        'kategoria': fields.Integer
    }
    class Dish_api(Resource):
        @marshal_with(resource_fields)
        def get(self, input=None):
            if input is None:
                dishes = Przepisy.query.all()
            else:
                if input.isdigit():
                    dishes = Przepisy.query.filter_by(id=input).first()
                    dishes = [dishes]
                else:
                    dishes = Przepisy.query.filter_by(nazwa=input).first()
                    dishes = [dishes]
            for dish in dishes:
                holder_of_ingredients = dish.ListaSkladnikow
                holder_of_ingredients = holder_of_ingredients.split(' ')
                dish.ListaSkladnikow = ""
                for ingredient_number in holder_of_ingredients:
                    if ingredient_number != " ":
                        ingredient_number = int(ingredient_number)
                        name_of_ingredient = Skladniki.query.filter_by(id=ingredient_number).first()
                        name_of_ingredient = str(name_of_ingredient.Nazwa)
                        dish.ListaSkladnikow += name_of_ingredient + " "
            return dishes

        def post(self):
            user_input = request.get_json()
            if user_input is None:
                return {'message': 'No input data provided'}, 400
            if user_input.get('nazwa') is None or user_input.get('czas') is None or user_input.get('opis') is None or user_input.get('ListaSkladnikow') is None or user_input.get('przepis') is None:
                return {'message': 'Missing required field(s)'}, 400
            if user_input.get("ListasSkladnikow").isdigit():
                ingredients = int(user_input['ListaSkladnikow'])
            else:
                ingredients = user_input['ListaSkladnikow'].split(' ')
            end_ingredients = ""
            for x in ingredients:
                 if x != " ":
                    x = int(x)
                    if Skladniki.query.filter_by(id=x).first() == None:
                        new_ingredient = Skladniki.filter_by(id=x).first()
                        new_ingredient = str(new_ingredient.Nazwa)
                        end_ingredients+=new_ingredient+" "
            new_dish = Przepisy(nazwa=user_input['nazwa'], czas=user_input['czas'], opis=user_input['opis'], ListaSkladnikow=end_ingredients, przepis=user_input['przepis'])
            db.session.add(new_dish)
            db.session.commit()
            return {'message': 'New dish created'}, 201
        def delete(self,input):
            dish = Przepisy.query.filter_by(id=input).first()
            if dish is None:
                return {'message': 'Dish not found'}, 404
            db.session.delete(dish)
            db.session.commit()
            return {'message': 'Dish deleted'}, 200
        def put(self,input):
            user_input = request.get_json()
            if input.isdigit():
                input = int(input)
                dish = Przepisy.query.filter_by(id=input).first()
            else:
                dish = Przepisy.query.filter_by(nazwa=input).first()
            if dish is None:
                return {'message': 'Dish not found'}, 404
            if user_input.get('nazwa') is None or user_input.get('czas') is None or user_input.get('opis') is None or user_input.get('ListaSkladnikow') is None or user_input.get('przepis') is None:
                return {'message': 'Missing required field(s)'}, 400
            else:
                dish.nazwa = user_input['nazwa']
                dish.czas = user_input['czas']
                dish.opis = user_input['opis']
                dish.ListaSkladnikow = user_input['ListaSkladnikow']
                dish.przepis = user_input['przepis']
                db.session.commit()
                return {'message': 'Dish updated'}, 200


    class Ingredients_api(Resource):
        @marshal_with(resource_fields2)
        def get(self,input=None):
            if input is None:
                ingredients = Skladniki.query.all()
            else:
                if input.isdigit():
                    ingredients = Skladniki.query.filter_by(id=input).first()
                else:
                    ingredients = Skladniki.query.filter_by(Nazwa=input).first()
            return ingredients
        def post(self):
            user_input = request.get_json()
            if user_input is None:
                return {'message': 'No input data provided'}, 400
            if user_input.get('Nazwa') is None or user_input.get('kategoria') is None:
                return {'message': 'Missing required field(s)'}, 400
            else:
                new_ingredient = Skladniki(Nazwa=user_input['Nazwa'], kategoria=user_input['kategoria'])
                db.session.add(new_ingredient)
                db.session.commit()
                return {'message': 'New ingredient created'}, 201
        def delete(self,input):
            if input.isdigit():
                input = int(input)
                ingredient = Skladniki.query.filter_by(id=input).first()
            else:
                ingredient = Skladniki.query.filter_by(Nazwa=input).first()
            if ingredient is None:
                return {'message': 'Ingredient not found'}, 404
            db.session.delete(ingredient)
            db.session.commit()
            return {'message': 'Ingredient deleted'}, 200
        def put(self,input):
            user_input = request.get_json()
            if input.isdigit():
                input = int(input)
                ingredient = Skladniki.query.filter_by(id=input).first()
            else:
                ingredient = Skladniki.query.filter_by(Nazwa=input).first()
            if ingredient is None:
                return {'message': 'Ingredient not found'}, 404
            if user_input.get('Nazwa') is None or user_input.get('kategoria') is None:
                return {'message': 'Missing required field(s)'}, 400
            else:
                ingredient.Nazwa = user_input['Nazwa']
                ingredient.kategoria = user_input['kategoria']
                db.session.commit()
                return {'message': 'Ingredient updated'}, 200

    api.add_resource(Dish_api, '/API/przepisy/<input>', '/API/przepisy')
    api.add_resource(Ingredients_api, '/API/skladniki', '/API/skladniki/<input>')

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app
