from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for, session
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
    print(current_user)
    if Admin.query.filter_by(name="Admin").first() == None:
        admin = Admin(name="Admin", password=generate_password_hash("4321"))
        db.session.add(admin)
        db.session.commit()
    skladniki = db.session.query(Skladniki)
    if request.method == 'POST' and request.form != None:
        SkladnikiUsera = ""
        id = 0
        f = request.form
        print(f)
        listakey = []
        sessionstarter=""
        for key in f:
            for value in f.getlist(key):
                sessionstarter+=str(key)+" "
                keys = int(key)
                listakey.append(keys)
        listakey.sort()
        session['skladniki'] = sessionstarter
        print(sessionstarter)
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
    if session.get('skladniki') != None:
        SkladnikiUsera = ""
        id = 0
        f = session['skladniki'].split()
        listakey = []
        for key in f:
            if key != " ":
                keys = int(key)
                listakey.append(keys)
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
                               SkladnikiWybrane=skladnikiWybrane, )
    else:
        return render_template('index.html', Skladnikiz=skladniki)


# @views.route('/usuwanie/<int:id>', methods=['POST', 'GET'])
# def indexUsuwanie(id):
#     if session.get('skladniki') == None:
#         return redirect('/')
#     doUsunięcia=id
#     sessia=session['skladniki']
#     nowaSessia=""
#     array = sessia.split()
#     array.remove(str(doUsunięcia))
#     for key in array:
#         if key != " ":
#             keys = int(key)
#             nowaSessia += str(keys) + " "
#     session['skladniki'] = nowaSessia
#     return redirect('/')

@views.route('/danie/<int:id>', methods=['POST', 'GET'])
def indexDanie(id):
    danie = db.session.query(Przepisy).filter(Przepisy.id == id).first()
    return render_template('dishSite.html', danie=danie,url_path=url_for('static',filename='img/'+str(danie.id)+'.png'))
