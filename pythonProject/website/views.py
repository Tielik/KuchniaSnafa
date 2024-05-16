import werkzeug
from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for, session
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, engine
from . import db
from .models import Admin, Przepisy, Skladniki  # Skladniki Przepisy

views = Blueprint('views', __name__)

"""
A function that selects the right dishes based on the provided user input.

Parameters:
user_input: The user input containing the ingredients to select.

Returns:
Tuple: A tuple containing two elements:
        - dania_z_bazy_danych (list of Przepisy objects or None): A list of dishes from the database that match the selected ingredients
             or None if no matching dishes were found.
        - skladniki_wybrane (list of Skladniki objects): The selected ingredients.
"""
def select_right_dishes(user_input):
    lista_wybranych_id = []
    # transform user_input to list
    if type(user_input) == werkzeug.datastructures.structures.ImmutableMultiDict :  # user_input
        session_zapisywacz = ""
        for key in user_input:
            for value in user_input.getlist(key):
                session_zapisywacz += str(key) + " "
                keys = int(key)
                lista_wybranych_id.append(keys)
        lista_wybranych_id.sort()
        session['skladniki'] = session_zapisywacz
    else:
        user_input = user_input.split()
        for x in user_input:
            lista_wybranych_id.append(int(x))
    # select right ingredients based of id in lista_wybranych_id
    nadzbior_uzytkownika = set(lista_wybranych_id)
    skladniki_wybrane = db.session.query(Skladniki).filter(Skladniki.id.in_(lista_wybranych_id)).all()
    dania = db.session.query(Przepisy).all()
    lista_dan = []
    for danie in dania:
        lista = danie.ListaSkladnikow
        lista.split()
        lista_int = []
        for y in lista:
            if y != " ":
                y = int(y)
                lista_int.append(y)
        nadzbior_dania = set(lista_int)
        if len(lista_wybranych_id) >= len(lista_int):
            if nadzbior_uzytkownika.issuperset(nadzbior_dania):
                lista_dan.append(danie.id)
    if len(lista_dan) != 0:
        dania_z_bazy_danych = db.session.query(Przepisy).filter(Przepisy.id.in_(lista_dan)).all()
    else:
        dania_z_bazy_danych = None
    return dania_z_bazy_danych, skladniki_wybrane

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
    skladniki = db.session.query(Skladniki)
    if request.method == 'POST' and request.form != None:
        form_input=request.form
        dania_z_Bazy_Danych,skladniki_wybrane = select_right_dishes(form_input)
        return render_template('index.html', form=form_input, dania=dania_z_Bazy_Danych, Skladnikiz=skladniki,
                               SkladnikiWybrane=skladniki_wybrane)
    if session.get('skladniki') != None:
        form_input = session.get('skladniki')
        dania_z_Bazy_Danych,skladniki_wybrane = select_right_dishes(form_input)
        return render_template('index.html', form=form_input, dania=dania_z_Bazy_Danych, Skladnikiz=skladniki,
                               SkladnikiWybrane=skladniki_wybrane)
    else:
        return render_template('index.html', Skladnikiz=skladniki)


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
    skladniki= db.session.query(Skladniki)
    danie= db.session.query(Przepisy).filter(Przepisy.id == id).first()
    return render_template('dishSite.html', skladniki=skladniki, danie=danie,url_path=url_for('static',filename='img/'+str(danie.id)+'.png'))

@views.route('/api')
def api():
    return render_template('api.html')#trzeba zrobić instrukcje