import werkzeug
from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for, session
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, engine
from . import db
from .models import Admin, Przepisy, Skladniki  # Skladniki Przepisy
import uuid
from .api import api_holder

views = Blueprint('views', __name__)

"""
A function that selects the right dishes based on the provided user input.

Parameters:
user_input: The user input containing the ingredients to select.

Returns:
Tuple: A tuple containing two elements:
        - dish_from_db (list of Przepisy objects or None): A list of dishes from the database that match the selected ingredients
             or None if no matching dishes were found.
        - chosen_ingredient (list of Skladniki objects): The selected ingredients.
"""
def select_right_dishes(user_input):
    list_of_chosen_id = []
    # transform user_input to list
    if type(user_input) == werkzeug.datastructures.structures.ImmutableMultiDict :  # user_input
        session_saver = ""
        for key in user_input:
            for value in user_input.getlist(key):
                session_saver += str(key) + " "
                keys = int(key)
                list_of_chosen_id.append(keys)
        list_of_chosen_id.sort()
        session['skladniki'] = session_saver
    else:
        user_input = user_input.split()
        for x in user_input:
            list_of_chosen_id.append(int(x))
    # select right ingredients based of id in list_of_chosen_id
    super_set_user = set(list_of_chosen_id)
    chosen_ingredient = db.session.query(Skladniki).filter(Skladniki.id.in_(list_of_chosen_id)).all()
    dishes = db.session.query(Przepisy).all()
    list_of_dishes = []
    for dish in dishes:
        lists = dish.Ingredients
        lists.split()
        lista_int = []
        for y in lists:
            if y != " ":
                y = int(y)
                lista_int.append(y)
        nadzbior_dania = set(lista_int)
        if len(list_of_chosen_id) >= len(lista_int):
            if super_set_user.issuperset(nadzbior_dania):
                list_of_dishes.append(dish.id)
    if len(list_of_dishes) != 0:
        dish_from_db = db.session.query(Przepisy).filter(Przepisy.id.in_(list_of_dishes)).all()
    else:
        dish_from_db = None
    return dish_from_db, chosen_ingredient

'''
a view that renders the index.html template
if admin is not in database it is created with name "Admin" and password "4321"

if the request method is POST and the form is not None, the select_right_dishes function is called
and the returned tuple is passed to the index.html template
if the request method is GET and session is not empty the session is passed to the select_right_dishes
 and output of select_right_dishes is passed to template


returns: the rendered index.html template
'''
@views.route('/', methods=['POST', 'GET'])
def index():
    if Admin.query.filter_by(name="Admin").first() == None:
        admin = Admin(name="Admin", password=generate_password_hash("4321"))
        db.session.add(admin)
        db.session.commit()
    ingredients = db.session.query(Skladniki)
    if request.method == 'POST' and request.form != None:
        form_input=request.form
        dishes_from_db,chosen_ingredient = select_right_dishes(form_input)
        return render_template('index.html', form=form_input, dania=dishes_from_db, Skladnikiz=ingredients,
                               SkladnikiWybrane=chosen_ingredient)
    if session.get('skladniki') != None:
        form_input = session.get('skladniki')
        dishes_from_db,chosen_ingredient = select_right_dishes(form_input)
        return render_template('index.html', form=form_input, dania=dishes_from_db, Skladnikiz=ingredients,
                               SkladnikiWybrane=chosen_ingredient)
    else:
        return render_template('index.html', Skladnikiz=ingredients)


    """
    A function that handles requests to display a specific dish based on the provided ID.
s
    Parameters:
    id (int): The ID of the dish to display.

    Returns:
    render_template: The rendered template for the dish site.
    """
@views.route('/danie/<int:id>', methods=['POST', 'GET'])
def indexDanie(id):
    ingredients= db.session.query(Skladniki)
    dish= db.session.query(Przepisy).filter(Przepisy.id == id).first()
    return render_template('dishSite.html', skladniki=ingredients, danie=dish,url_path=url_for('static',filename='img/'+str(dish.id)+'.png'))

@views.route('/api')
def api():
    if current_user.is_authenticated:
        return render_template('apiAdmin.html')
    else:
        return render_template('api.html')

@views.route('/api/tokenGenerator')
def tokenGenerator():
    api_holder.append(str(uuid.uuid4()))
    return jsonify({'token': api_holder[-1],"WARNING": "THIS WILL NOT BE SHOW AGAIN REMEMBER THIS TOKEN"})
