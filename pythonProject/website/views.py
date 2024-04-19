from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, engine
from . import db
from .models import Admin, Przepisy, Skladniki  # Skladniki Przepisy

views = Blueprint('views', __name__)


# admin = Admin(name="Admin", password=generate_password_hash("1234"))
# db.session.add(admin)
# db.session.commit()
@views.route('/', methods=['POST', 'GET'])
def index():
    if Admin.query.filter_by(name="Admin").first() == None:
        admin = Admin(name="Admin", password=generate_password_hash("4321"))
        db.session.add(admin)
        db.session.commit()
    skladniki = db.session.query(Skladniki)
    #id sesja istnieje zró to co poniżej ale też dodaj do sesji czego ni ma
    if request.method == 'POST' and request.form != None:
        SkladnikiUsera = ""
        id = 0
        f = request.form

        listakey = []
        for key in f:
            for value in f.getlist(key):
                keys = int(key)
                listakey.append(keys)
                #session[str(key)] = key
        listakey.sort()
        for x in listakey:
            if len(listakey) - 1 > id:
                lol = key + " "
                SkladnikiUsera += lol
                id += 1
            else:
                SkladnikiUsera += key
        setUser = set(listakey)
        skladnikiWybrane = db.session.query(Skladniki).filter(Skladniki.id.in_(listakey)).all()
        Dania = db.session.query(Przepisy).all()
        listaDan = []
        for x in Dania:
            lista = x.ListaSkladnikow
            lista.split()
            listaInt = []
            for y in lista:
                if y != " ":
                    y = int(y)
                    listaInt.append(y)
            setDanie = set(listaInt)
            if len(listakey) >= len(listaInt):
                if setUser.issuperset(setDanie):
                    listaDan.append(x.id)
        if len(listaDan) != 0:
            daniaDB = db.session.query(Przepisy).filter(Przepisy.id.in_(listaDan)).all()
        else:
            daniaDB = None
        return render_template('index.html', form=f, dania=daniaDB, Skladnikiz=skladniki,
                               SkladnikiWybrane=skladnikiWybrane)
    return render_template('index.html', Skladnikiz=skladniki)

@views.route('/danie/<int:id>', methods=['POST', 'GET'])
def indexDanie(id):
    danie = db.session.query(Przepisy).filter(Przepisy.id == id).first()
    return render_template('dishSite.html', danie=danie,url_path=url_for('static',filename='img/'+str(danie.id)+'.png'))

#uzywaz to jak chcesz cos usunąć z listy składników
# @views.route('/deleteIngredient/<int:id>', methods=['POST', 'GET'])
# def usuwanieZSessionAndWebsite(id):
#     session.pop(id, None)
#     #


