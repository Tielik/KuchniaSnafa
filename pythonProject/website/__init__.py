from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, Resource, fields, marshal_with
import sqlite3
from flask import g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"
"""
Initialize and configure th.e Flask app with necessary settings, blueprints, models, and resources. 
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

    auth = HTTPBasicAuth()

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

    @auth.verify_password
    def verify_password(username, password):
        if Admin.query.filter_by(name=username).first() is not None:
            user=Admin.query.filter_by(name=username).first()
            if check_password_hash(user.password, password):
                return True
        else:
            return False

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

    #wytestować
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
            if dishes is None:
                return {"wiadomość": 'Danie nie znalezione'}, 404
            for dish in dishes:
                holder_of_ingredients = dish.ListaSkladnikow.split(' ')
                holder_of_ingredients=[int(i) for i in holder_of_ingredients]
                dish.ListaSkladnikow = ""
                for ingredient_number in holder_of_ingredients:
                    if ingredient_number != '' or ingredient_number !=" ":
                        name_of_ingredient = Skladniki.query.filter_by(id=ingredient_number).first()
                        name_of_ingredient = str(name_of_ingredient.Nazwa)
                        dish.ListaSkladnikow += name_of_ingredient + " "
            return dishes

        @auth.login_required
        def post(self):
            user_input = request.get_json()
            if user_input is None:
                return {"wiadomość": 'Brak danych wejśiowych'}, 400
            if user_input.get('nazwa') is None or user_input.get('czas') is None or user_input.get('opis') is None or user_input.get('ListaSkladnikow') is None or user_input.get('przepis') is None:
                return {"wiadomość": 'Brak wymaganych pól'}, 400
            if str(user_input.get("ListasSkladnikow")).isdigit():
                ingredients = int(user_input['ListaSkladnikow'])
                ingredients =[ingredients]
            else:
                ingredients = str(user_input['ListaSkladnikow']).split(' ')
            end_ingredients = ""
            print(ingredients)
            for x in ingredients:
                 if x != " ":
                    x=str(x)
                    if Skladniki.query.filter_by(Nazwa=x).first() != None:
                        new_ingredient = Skladniki.query.filter_by(Nazwa=x).first()
                        new_ingredient = str(new_ingredient.id)
                        end_ingredients+=new_ingredient+" "
                    if x.isdigit() and Skladniki.query.filter_by(id=x).first() != None:
                        new_ingredient = x
                        end_ingredients += new_ingredient + " "
                    if Skladniki.query.filter_by(Nazwa=x).first() == None and x.isdigit()==False and Skladniki.query.filter_by(id=x).first() == None :
                        return {"wiadomość": 'Nie znaleziono składnika'}, 404
            new_dish = Przepisy(nazwa=user_input['nazwa'], czas=user_input['czas'], opis=user_input['opis'], ListaSkladnikow=end_ingredients, przepis=user_input['przepis'])
            db.session.add(new_dish)
            db.session.commit()
            return {"wiadomość": 'Dodano do bazy pomyślnie'}, 201

        @auth.login_required
        def delete(self,input):
            if input.isdigit():
                input = int(input)
                dish = Przepisy.query.filter_by(id=input).first()
            else:
                name=str(input)
                dish = Przepisy.query.filter_by(nazwa=name).first()
            if dish is None:
                return {"wiadomość": 'Nie znaleziono dania na podstawie danych wejśiowych'}, 404
            db.session.delete(dish)
            db.session.commit()
            return {"wiadomość": 'Danie usunięto poprawnie'}, 200

        @auth.login_required
        def put(self,input):
            user_input = request.get_json()
            if input.isdigit():
                input = int(input)
                dish = Przepisy.query.filter_by(id=input).first()
            else:
                dish = Przepisy.query.filter_by(nazwa=input).first()
            if dish is None:
                return {"wiadomość": 'Nie znaleziono dania na podstawie danych wejśiowych'}, 404
            if user_input.get('nazwa') is None or user_input.get('czas') is None or user_input.get('opis') is None or user_input.get('ListaSkladnikow') is None or user_input.get('przepis') is None:
                return {"wiadomość": 'Brak wymaganych pól'}, 400
            if user_input.get("ListasSkladnikow").isdigit() == False:
                ingredients = user_input['ListaSkladnikow'].split(' ')
                end_ingrediens=""
                for x in ingredients:
                    if x !=" ":
                        if not x.isdigit():
                            x=str(x)
                            if Skladniki.query.filter_by(name=x).first() is None:
                                return {"wiadomość": 'Nie ma składnika o takiej nazwie'}, 400
                            else:
                                place_holder=Skladniki.query.filter_by(name=x).first()
                                end_ingrediens+=str(place_holder.id)+" "
                        else:
                            x=int(x)
                            if Skladniki.query.filter_by(id=x).first() is None:
                                return{"wiadomość": 'Nie ma takiego składnia o podanej nazwie'}, 404
                            end_ingrediens+=x+" "
            else:
                ingredients=user_input['ListaSkladnikow']
            if user_input['nazwa'] is not None:
                dish.nazwa = user_input['nazwa']
            if user_input['czas'] is not None:
                dish.czas = user_input['czas']
            if user_input['opis'] is not None:
                dish.opis = user_input['opis']
            if user_input['ListaSkladnikow'] is not None:
                dish.ListaSkladnikow = end_ingrediens
            if user_input['przepis'] is not None:
                dish.przepis = user_input['przepis']
            db.session.commit()
            return {"wiadomość": 'Zmieniono danie poprawnie'}, 200


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
            if ingredients is not  None:
                return ingredients
            else:
                return {"wiadomość": 'Nie ma takiego składnika'}, 400

        @auth.login_required
        def post(self):
            user_input = request.get_json()
            if user_input is None:
                return {"wiadomość": 'Brak danych wejściowych'}, 400
            if user_input.get('Nazwa') is None or user_input.get('kategoria') is None:
                return {"wiadomość": 'Brak wymaganych pól'}, 400
            else:
                if user_input.get('Nazwa').isdigit() or user_input.get('kategoria').isdigit()== False or int(user_input.get("kategoria"))>9 or int(user_input.get("kategoria"))<=0:
                    return {"wiadomość": 'nazwa nie moze mieć cyfr, a kategoria musi być cyfrą od 0 do 8'}, 404
                new_ingredient = Skladniki(Nazwa=user_input['Nazwa'], kategoria=user_input['kategoria'])
                db.session.add(new_ingredient)
                db.session.commit()
                return {"wiadomość": 'Stworzono nowy składnik pomyslnie'}, 201

        @auth.login_required
        def delete(self,input):
            if input.isdigit():
                input = int(input)
                ingredient = Skladniki.query.filter_by(id=input).first()
            else:
                ingredient = Skladniki.query.filter_by(Nazwa=input).first()
            if ingredient is None:
                return {"wiadomość": 'Nie znaleziono składnika'}, 404
            db.session.delete(ingredient)
            db.session.commit()
            dishes = Przepisy.query.all()
            for dish in dishes:
                print(dish)
                ingredients_holder=dish.ListaSkladnikow
                ingredients_holder.split(' ')
                for x in ingredients_holder:
                    if x != " " or "":
                        if int(x)==int(input):
                            db.session.delete(dish)
                            db.session.commit()
            return {"wiadomość": 'Poprawnie usunięto składnik'}, 200

        @auth.login_required
        def put(self,input):
            user_input = request.get_json()
            if input.isdigit():
                input = int(input)
                ingredient = Skladniki.query.filter_by(id=input).first()
            else:
                ingredient = Skladniki.query.filter_by(Nazwa=input).first()
            if ingredient is None:
                return {"wiadomość": 'Nie znaleziono składnika do modyfikacji'}, 404
            if user_input.get('Nazwa') is None or user_input.get('kategoria') is None:
                return {"wiadomość": 'Brak wymaganych pól'}, 400
            else:
                if user_input.get('Nazwa').isdigit() or user_input.get('kategoria').isdigit()==False or int(user_input.get("kategoria"))>9 or int(user_input.get("kategoria"))<=0:
                    return {"wiadomość": 'nazwa nie moze mieć cyfr a kategoria musi mieć cyfry'}, 404
                if user_input['Nazwa'] is not None:
                    ingredient.Nazwa = user_input['Nazwa']
                if user_input['kategoria'] is not None:
                    ingredient.kategoria = user_input['kategoria']
                db.session.commit()
                return {"wiadomość": 'Pomyślnie zmieniono składnik'}, 200

    api.add_resource(Dish_api, '/API/przepisy/<input>', '/API/przepisy')
    api.add_resource(Ingredients_api, '/API/skladniki', '/API/skladniki/<input>')

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app
