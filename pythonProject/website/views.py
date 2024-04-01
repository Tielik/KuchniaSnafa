from flask import Blueprint, render_template, request, flash, json, jsonify, redirect
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
    if request.method == 'POST' and request.form != None:
        SkladnikiUsera=""
        id=0
        f = request.form
        listakey=[]
        for key in f:
            for value in f.getlist(key):
                keys=int(key)
                listakey.append(keys)
        listakey.sort()
        for x in listakey:
            if len(listakey)-1>id:
                lol=key+" "
                SkladnikiUsera+=lol
                id += 1
            else:
                SkladnikiUsera+=key
        setUser=set(listakey)
        Dania=db.session.query(Przepisy).all()
        listaDan=[]
        for x in Dania:
            lista=x.ListaSkladnikow
            lista.split()
            listaInt=[]
            for y in lista:
                if y!=" ":
                    y=int(y)
                    listaInt.append(y)
            setDanie=set(listaInt)
            if len(listaInt)>=len(listakey):
                if setDanie.issuperset(setUser):
                    listaDan.append(x.id)
            if len(listakey)>len(listaInt):
                if setUser.issuperset(setDanie):
                    listaDan.append(x.id)
        if len(listaDan)!=0:
            daniaDB=db.session.query(Przepisy).filter(Przepisy.id.in_(listaDan)).all()
        else:
            daniaDB=None
        return render_template('index.html', form=f,dania=daniaDB)
    return render_template('index.html')
#PASY Admin h:1234

@views.route('/admin', methods=['POST', 'GET'])
def admin():
    if current_user.is_authenticated:
        if db.session.query(Przepisy).count() >= 1:
            przepisyz = db.session.query(Przepisy)
        else:
            przepisyz = None
        if db.session.query(Skladniki).count() >= 1:
            skladniki = db.session.query(Skladniki)
        else:
            skladniki = None
        return render_template('admin.html',Przepisy=przepisyz,Skladniki=skladniki)
    #print(db.session.query(Przepisy).count())
    if request.method == 'POST':
        name = request.form.get('Admin')
        password = request.form.get('password')
        if db.session.query(db.exists().where(Admin.name == name)).scalar():
            user = Admin.query.filter_by(name=name).first()
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if db.session.query(Przepisy).count() >= 1:
                    przepisyz = db.session.query(Przepisy)
                else:
                    przepisyz = None
                if db.session.query(Skladniki).count() >= 1:
                    skladniki = db.session.query(Skladniki)
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
    if current_user.is_authenticated:
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
        return render_template('przepisy.html',)
@views.route('/admin/Skladniki', methods=['POST', 'GET'])
def skladniki():
    if current_user.is_authenticated:
        if request.method == 'POST':
            Nazwa=request.form.get('Nazwa')
            kategoria=request.form.get('kategoria')
            skladniki = Skladniki(Nazwa=Nazwa,kategoria=kategoria)
            db.session.add(skladniki)
            db.session.commit()
            flash('Skladnik został dodany!', category='success')
            return redirect('/admin')
        return render_template('skladniki.html')

@views.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
@views.route('/admin/delete/przepis/<int:id>')
def delete(id):
    if current_user.is_authenticated:
        przepis = Przepisy.query.filter_by(id=id).first()
        db.session.delete(przepis)
        db.session.commit()
        flash('Przepis został usunięty!', category='success')
        return redirect('/admin')
@views.route('/admin/delete/skladnik/<int:id>')
def deleteS(id):
    if current_user.is_authenticated:
        skladnik = Skladniki.query.filter_by(id=id).first()
        db.session.delete(skladnik)
        db.session.commit()
        flash('Skłądnik został usunięty!', category='success')
        return redirect('/admin')

@views.route('/admin/edit/skladnik/<int:id>', methods=['POST', 'GET'])
def edit(id):
        if current_user.is_authenticated:
            skladnik = Skladniki.query.filter_by(id=id).first()
            if request.method == 'POST':
                skladnik.Nazwa = request.form.get('Nazwa')
                skladnik.kategoria = request.form.get('kategoria')
                db.session.commit()
                flash('Skladnik został edytowany!', category='success')
                return redirect('/admin')
            return render_template('editSkladnik.html',skladnik=skladnik)
@views.route('/admin/edit/przepis/<int:id>', methods=['POST', 'GET'])
def editP(id):
    if current_user.is_authenticated:
        przepis = Przepisy.query.filter_by(id=id).first()
        if request.method == 'POST':
            przepis.nazwa = request.form.get('nazwa')
            przepis.czas = request.form.get('czas')
            przepis.opis = request.form.get('opis')
            przepis.skladniki = request.form.get('skladniki')
            przepis.przepis = request.form.get('przepis')
            przepis.ListaSkladnikow = request.form.get('lista')
            db.session.commit()
            flash('Przepis został edytowany!', category='success')
            return redirect('/admin')
        return render_template('editPrzepis.html',przepis=przepis)



