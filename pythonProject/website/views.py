from flask import Blueprint, render_template, request, flash, json, jsonify, redirect
from flask_login import login_required, logout_user, current_user
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
    if request.method == 'POST' and request.form != None:
        SkladnikiUsera=""
        id=0
        f = request.form
        for key in f:
            for value in f.getlist(key):
                print(key, ":", value)
                print(f)
                if len(f)-1>id:
                    lol=key+" "
                    SkladnikiUsera+=lol
                    id += 1
                else:
                    SkladnikiUsera+=key
        daniaDB=db.session.query(Przepisy).filter_by(ListaSkladnikow=SkladnikiUsera).all()
        return render_template('index.html', form=f,dania=daniaDB)
    return render_template('index.html')
#PASY Admin h:1234

@views.route('/admin', methods=['POST', 'GET'])
def admin():
    #print(db.session.query(Przepisy).count())
    if request.method == 'POST':
        name = request.form.get('Admin')
        password = request.form.get('password')
        if db.session.query(db.exists().where(Admin.name == name)).scalar():
            user = Admin.query.filter_by(name=name).first()
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                if db.session.query(Przepisy).count() >= 1:
                    przepisyz = db.session.query(Przepisy)
                    for x in przepisyz:
                        print(x.id, x.nazwa, x.czas, x.opis, x.skladniki, x.przepis, x.ListaSkladnikow)
                else:
                    przepisyz = None
                if db.session.query(Skladniki).count() >= 1:
                    skladniki = select(Skladniki)
                else:
                    skladniki = None
                return render_template('admin.html',Przepisy=przepisyz,Skladniki=skladniki)
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template('Login.html')
        else:
            flash('Name does not exist.', category='error')
            return render_template('Login.html')

    else:
        return render_template('Login.html')
@views.route('/admin/Przepisy', methods=['POST', 'GET'])
def przepisy():
    if request.method == 'POST':
        nazwa=request.form.get('nazwa')
        czas=request.form.get('czas')
        opis=request.form.get('opis')
        skladniki=request.form.get('skladniki')
        przepis=request.form.get('przepis')
        ListaSkladnikow=request.form.get('lista')
        przepis = Przepisy(nazwa=nazwa,czas=czas,opis=opis,skladniki=skladniki,przepis=przepis,ListaSkladnikow=ListaSkladnikow)
        db.session.add(przepis)
        db.session.commit()
        flash('Przepis został dodany!', category='success')
        return redirect('/admin')
    return render_template('przepisy.html')
@views.route('/admin/Skladniki', methods=['POST', 'GET'])
def skladniki():
    if request.method == 'POST':
        pass
    return redirect('/admin')