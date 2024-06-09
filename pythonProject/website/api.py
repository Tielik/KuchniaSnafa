from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, Resource, fields, marshal_with, abort
import sqlite3
from flask import g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from . import db
from .models import Admin, Przepisy, Skladniki

auth = HTTPBasicAuth()

"""
A function to verify the password for a given username.

Parameters:
    - username: A string representing the username to verify.
    - password: A string representing the password to check against the user's stored password hash.

Returns:
    - True if the password matches the stored hash for the given username, False otherwise.
"""
@auth.verify_password
def verify_password(username, password):
    if Admin.query.filter_by(name=username).first() is not None:
        user = Admin.query.filter_by(name=username).first()
        if check_password_hash(user.password, password):
            return True
    else:
        return False

    """
    A function to check if the user input contains valid ingredient data based on specific criteria.

    Parameters:
        - user_input: A dictionary containing 'Nazwa' and 'kategoria' keys for ingredient name and category.

    Returns:
        - True if the input is a valid ingredient, False otherwise.
    """
def is_ingredient(user_input):
    if str(user_input.get('Nazwa')).isdigit() or str(user_input.get('kategoria')).isdigit() == False or int(
            user_input.get("kategoria")) > 9 or int(user_input.get("kategoria")) <= 0:
            return False
    else:
        return True

    """
    A function to remove dishes with a matching ingredient based on the input.

    Parameters:
        - input: The ingredient ID to match for removal.

    Returns:
        This function does not return anything.
    """
def  dishes_with_matching_ingredient_remover(input):
    dishes = Przepisy.query.all()
    for dish in dishes:
        print(dish)
        ingredients_holder = dish.Ingredients
        ingredients_holder.split(' ')
        for x in ingredients_holder:
            if x.isdigit():
                if int(x) == int(input):
                    db.session.delete(dish)
                    db.session.commit()

    """
    A function to match dish input and retrieve dishes based on the input provided.

    Parameters:
        - user_input: The input provided by the user to match dishes.

    Returns:
        A list of dishes matching the user input.
    """
def dish_input_matcher(user_input):
    if user_input.isdigit():
        dishes = Przepisy.query.filter_by(id=user_input).first()
        dishes = [dishes]
    else:
        dishes = Przepisy.query.filter_by(nazwa=user_input).first()
        dishes = [dishes]
    return dishes

    """
    A function to match ingredients and generate a new list based on the input ingredients.

    Parameters:
        - ingredients: A list of ingredients to match.

    Returns:
        A string containing the matched ingredient IDs.
    """
def ingredients_input_matcher(user_input):
    if user_input.isdigit():
        ingredients = Skladniki.query.filter_by(id=user_input).first()
        ingredients = [ingredients]
    else:
        ingredients = Skladniki.query.filter_by(nazwa=user_input).first()
        ingredients = [ingredients]
    return ingredients

    """
    A function to match ingredients and generate a new list based on the input ingredients.

    Parameters:
        - ingredients: A list of ingredients to match.

    Returns:
        A string containing the matched ingredient IDs.
    """
def ingredients_matcher(ingredients):
    end_ingredients = ""
    for x in ingredients:
        if x != " ":
            x = str(x)
            if Skladniki.query.filter_by(Nazwa=x).first() != None:
                new_ingredient = Skladniki.query.filter_by(Nazwa=x).first()
                new_ingredient = str(new_ingredient.id)
                end_ingredients += new_ingredient + " "
            if x.isdigit() and Skladniki.query.filter_by(id=x).first() != None:
                new_ingredient = x
                end_ingredients += new_ingredient + " "
    return end_ingredients


api_holder=[]
def require_api_key(f):
    def decorated_function(*args,**kwargs):
        print(api_holder)
        api_key=request.headers.get("x-api-key")
        if not api_key:
            api_key=request.args.get('api_key')
        if api_key not in api_holder:
            abort(404,message="Mising Api key, ad api like this: ?api_key=de99cb8c-976e-4c4f-9692-839f88338fcc")
        return f(*args,**kwargs)
    decorated_function.__name__=f.__name__
    return decorated_function
#templates tha api will return if get will be called
resource_fields = {
    'id': fields.Integer,
    'nazwa': fields.String,
    'Time': fields.String,
    'opis': fields.String,
    'Ingredients': fields.String,
    'przepis': fields.String,
}
resource_fields2 = {
    'id': fields.Integer,
    'Nazwa': fields.String,
    'kategoria': fields.Integer
}


#wymienik na resource fields :< albo ogarnij dokładnie co marshal robi
# tokeny tak: przycisk na stronie z instrukcją dostajesz token i by zrobić geta potrzebujesz tokena :>


class Dish_api(Resource):

    """
    A function to retrieve dishes based on the input provided.

    Parameters:
        - input: The input to match dishes.

    Returns:
        A list of dishes matching the input.
    """
    @marshal_with(resource_fields)
    @require_api_key
    def get(self, input=None):
        api_key=request.headers.get("x-api-key")
        print(api_key)
        print("asdsad")
        if input is None:
            dishes = Przepisy.query.all()
        else:
            dishes=dish_input_matcher(input)
        print(dishes)
        if dishes == [None] or dishes == []:
            abort(404, message="Danie/a nie znalezione")
        else:
            for dish in dishes:
                holder_of_ingredients = dish.Ingredients.split(' ')
                for x in holder_of_ingredients:
                    if x.isdigit():
                        x=int(x)          
                dish.Ingredients = ""
                for ingredient_number in holder_of_ingredients:
                    if ingredient_number.isdigit():
                        name_of_ingredient = Skladniki.query.filter_by(id=ingredient_number).first()
                        name_of_ingredient = str(name_of_ingredient.Nazwa)
                        dish.Ingredients += name_of_ingredient + " "
            return dishes

        """
        A function to handle the post request for creating a new dish.
        It checks for required fields in the user input and processes the ingredients.
        
        Parameters: None
        
        Returns: A success message with a status code.
        """
    @auth.login_required
    def post(self):
        user_inputs = request.get_json()
        for user_input in user_inputs:
            if user_input is None:
                return {"wiadomość": 'Brak danych wejśiowych'}, 400
            if user_input['nazwa'] is None or user_input['Time'] is None or user_input['opis'] is None or user_input['Ingredients'] is None or user_input['przepis'] is None:
                return {"wiadomość": 'Brak wymaganych pól'}, 400
            if str(user_input["Ingredients"]).isdigit():
                ingredients = int(user_input['Ingredients'])
                ingredients = [ingredients]
            else:
                ingredients = str(user_input['Ingredients']).split(' ')

            end_ingredients = ingredients_matcher(ingredients)
            new_dish = Przepisy(nazwa=user_input['nazwa'], Time=user_input['Time'], opis=user_input['opis'],
                                Ingredients=end_ingredients, przepis=user_input['przepis'])
            db.session.add(new_dish)
            db.session.commit()
        return {"wiadomość": 'Dodano do bazy pomyślnie'}, 201

        """
        A function to delete a dish based on the input provided.

        Parameters:
            - input: The input to match the dish to be deleted.

        Returns:
            A message indicating the success or failure of the deletion process along with an appropriate status code.
        """
    @auth.login_required
    def delete(self, input):
        dish=dish_input_matcher(input)
        if dish == [None]:
            return {"wiadomość": 'Nie znaleziono dania na podstawie danych wejśiowych'}, 404
        db.session.delete(dish)
        db.session.commit()
        return {"wiadomość": 'Danie usunięto poprawnie'}, 200

        """
        A function to update a dish based on the input provided.

        Parameters:
            - input: The input to match the dish to be updated.

        Returns:
            A message indicating the success or failure of the update process along with an appropriate status code.
        """
    @auth.login_required
    def put(self, input):
        user_input = request.get_json()
        if user_input is list:
            return {"wiadomość": 'Edytować można tylko jeden element na raz'}, 400
        dishes=dish_input_matcher(input)
        print(dishes)
        if dishes == [None] or dishes is None:
            return {"wiadomość": 'Nie znaleziono dania na podstawie danych wejśiowych'}, 404
        if user_input is None:
            return {"wiadomość": 'Brak danych wejściowych'}, 400
        for dish in dishes:
            if str(user_input.get("ListasSkladnikow")).isdigit() == False:
                ingredients = user_input['Ingredients'].split(' ')
                end_ingredients =ingredients_matcher(ingredients)
            else:
                end_ingredients = user_input['Ingredients']
            if user_input['nazwa'] is not None:
                dish.nazwa = user_input['nazwa']
            if user_input['Time'] is not None:
                dish.Time = user_input['Time']
            if user_input['opis'] is not None:
                dish.opis = user_input['opis']
            if user_input['Ingredients'] is not None:
                dish.Ingredients = end_ingredients
            if user_input['przepis'] is not None:
                dish.przepis = user_input['przepis']
            db.session.commit()
        return {"wiadomość": 'Zmieniono danie poprawnie'}, 200


class Ingredients_api(Resource):
    """
    A function to retrieve ingredients based on the input provided.

    Parameters:
        - input: The input to match ingredients.

    Returns:
        A list of ingredients matching the input.
    """
    @marshal_with(resource_fields2)
    @require_api_key
    def get(self, input=None):
        if input is None:
            ingredients = Skladniki.query.all()
        else:
            ingredients=ingredients_input_matcher(input)
        if ingredients == []or ingredients ==[None]:
            abort(404, message="Nie ma składnika/ków o podanych parametrach")
        return ingredients

        """
        A function to create a new ingredient based on the user input provided.

        Parameters:
            - none

        Returns:
            A message indicating the success or failure of the creation process along with an appropriate status code.
        """
    @auth.login_required
    def post(self):
        user_inputs = request.get_json()
        user_inputs=[user_inputs]
        for user_input in user_inputs:
            if user_input is None:
                return {"wiadomość": 'Brak danych wejściowych'}, 400
            if user_input.get('Nazwa') is None or user_input.get('kategoria') is None:
                return {"wiadomość": 'Brak wymaganych pól'}, 400
            else:
                if is_ingredient(user_input) == False:
                    return {"wiadomość": 'nazwa nie moze mieć cyfr, a kategoria musi być cyfrą od 0 do 8'}, 404
                new_ingredient = Skladniki(Nazwa=user_input['Nazwa'], kategoria=user_input['kategoria'])
                db.session.add(new_ingredient)
                db.session.commit()
        return {"wiadomość": 'Stworzono nowy składnik pomyslnie'}, 201

        """
        A function to delete an ingredient based on the provided input.

        Parameters:
            - input: The input used to match the ingredient to be deleted.

        Returns:
            A message indicating the success or failure of the deletion process along with an appropriate status code.
        """
    @auth.login_required
    def delete(self, input):
        ingredients = ingredients_input_matcher(input)
        if ingredients == [None] or ingredients is None:
            return {"wiadomość": 'Nie znaleziono składnika'}, 404
        for ingredient in ingredients:
            db.session.delete(ingredient)
            db.session.commit()
        dishes_with_matching_ingredient_remover(input)
        return {"wiadomość": 'Poprawnie usunięto składnik'}, 200

        """
        A function to update an ingredient based on the provided input.

        Parameters:
            - input: The input used to match the ingredient to be updated.

        Returns:
            A message indicating the success or failure of the update process along with an appropriate status code.
        """
    @auth.login_required
    def put(self, input):
        user_input = request.get_json()
        ingredients = ingredients_input_matcher(input)
        if ingredients == [None] or ingredients is None:
            return {"wiadomość": 'Nie znaleziono składnika do modyfikacji'}, 404
        if user_input.get('Nazwa') is None or user_input.get('kategoria') is None:
            return {"wiadomość": 'Brak wymaganych pól'}, 400
        else:
            if is_ingredient(user_input) == False:
                return {"wiadomość": 'nazwa nie moze mieć cyfr a kategoria musi mieć cyfry'}, 404
            for ingredient in ingredients:
                if user_input['Nazwa'] is not None:
                    ingredient.Nazwa = user_input['Nazwa']
                if user_input['kategoria'] is not None:
                    ingredient.kategoria = user_input['kategoria']
            db.session.commit()
            return {"wiadomość": 'Pomyślnie zmieniono składnik'}, 200
