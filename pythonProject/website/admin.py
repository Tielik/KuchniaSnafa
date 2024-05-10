from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, session
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, engine
from . import db
from .models import Admin, Przepisy, Skladniki  # Skladniki Przepisy
import os

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['POST', 'GET'])
def Indexadmin():
    if current_user.is_authenticated:
        if db.session.query(Przepisy).count() >= 1:
            przepisyz = db.session.query(Przepisy)
        else:
            przepisyz = None
        if db.session.query(Skladniki).count() >= 1:
            skladniki = db.session.query(Skladniki)
        else:
            skladniki = None
        return render_template('admin.html', Przepisy=przepisyz, Skladniki=skladniki)
    # print(db.session.query(Przepisy).count())
    if request.method == 'POST':
        name = request.form.get('Admin')
        password = request.form.get('password')
        if db.session.query(db.exists().where(Admin.name == name)).scalar():
            user = Admin.query.filter_by(name=name).first()
            if check_password_hash(user.password, password):
                flash('Udało ci się zalogować!', category='success')
                login_user(user, remember=True)
                if db.session.query(Przepisy).count() >= 1:
                    przepisyz = db.session.query(Przepisy)
                else:
                    przepisyz = None
                if db.session.query(Skladniki).count() >= 1:
                    skladniki = db.session.query(Skladniki)
                else:
                    skladniki = None
                return render_template('admin.html', Przepisy=przepisyz, Skladniki=skladniki)
            else:
                flash('Nieprawidłowy login lub hasło', category='error')
                return render_template('login.html')
        else:
            flash('Nieprawidłowy login lub hasło', category='error')
            return render_template('login.html')

    else:
        return render_template('login.html')


@admin.route('/CLP', methods=['POST', 'GET'])
def changeOfPasword():
    if current_user.is_authenticated:
        admin = Admin.query.filter_by(name=current_user.name).first()
        if request.method == 'POST':
            name = request.form.get('Admin')
            password = request.form.get('password')
            user = Admin.query.filter_by(name=name).first()
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Zmieniono hasło', category='success')
            return redirect('/admin')
        return render_template('adminChange.html', admin=admin,
                               password=check_password_hash(current_user.password, admin.password))
    else:
        return redirect('/admin')


@admin.route('/Przepisy', methods=['POST', 'GET'])
def przepisy():
    if current_user.is_authenticated:
        if db.session.query(Skladniki).count() >= 1:
            skladniki = db.session.query(Skladniki)
        else:
            skladniki = None
            flash("By dodać danie trzeba najpierw wprowadzić składniki!", category="error")
            return redirect('/admin')
        if request.method == 'POST':
            nazwa = request.form.get('nazwa')
            czas = request.form.get('czas')
            opis = request.form.get('opis')
            skladniki = request.form.get('skladniki')
            przepis = request.form.get('przepis')
            ListaSkladnikow = request.form.getlist('lista')
            ListaSkladnikow = " ".join(ListaSkladnikow)
            przepis = Przepisy(nazwa=nazwa, czas=czas, opis=opis, skladniki=skladniki, przepis=przepis,
                               ListaSkladnikow=ListaSkladnikow)
            grafika = request.files['grafika']
            grafika_name = grafika.filename
            if grafika_name != '':
                grafika_ext = os.path.splitext(grafika_name)[1]
                if grafika_ext in ['.png', '.jpg', '.jpeg', '.webp']:
                    dishCounter=db.session.query(Przepisy).count()
                    dishCounter += 1
                    grafika_name = str(dishCounter)
                    grafika_name = grafika_name.replace(grafika_ext, '.png')
                    grafika.save(os.path.join('website/static/img', grafika_name))
                    db.session.add(przepis)
                    db.session.commit()
                    flash('Przepis został dodany!', category='success')
                    return redirect('/admin')
                else:
                    flash('Nieprawidłowy format grafiki!', category='error')
                    return redirect('/admin/Przepisy')
        return render_template('przepisy.html', skladniki=skladniki)
    return redirect('/')


@admin.route('/Skladniki', methods=['POST', 'GET'])
def skladniki():
    if current_user.is_authenticated:
        if request.method == 'POST':
            Nazwa = request.form.get('Nazwa')
            kategoria = request.form.get('kategoria')
            skladniki = Skladniki(Nazwa=Nazwa, kategoria=kategoria)
            db.session.add(skladniki)
            db.session.commit()
            flash('Skladnik został dodany!', category='success')
            return redirect('/admin')
        return render_template('skladniki.html')
    return redirect('/')


@admin.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    return redirect('/')


@admin.route('/delete/przepis/<int:id>')
def delete(id):
    if current_user.is_authenticated:
        przepis = Przepisy.query.filter_by(id=id).first()
        db.session.delete(przepis)
        db.session.commit()
        flash('Przepis został usunięty!', category='success')
        return redirect('/admin')
    return redirect('/')


@admin.route('/delete/skladnik/<int:id>')
def deleteS(id):
    if current_user.is_authenticated:
        skladnik = Skladniki.query.filter_by(id=id).first()
        db.session.delete(skladnik)
        db.session.commit()
        flash('Skłądnik został usunięty!', category='success')
        return redirect('/admin')
    return redirect('/')


@admin.route('/edit/skladnik/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if current_user.is_authenticated:
        skladnik = Skladniki.query.filter_by(id=id).first()
        if request.method == 'POST':
            skladnik.Nazwa = request.form.get('Nazwa')
            skladnik.kategoria = request.form.get('kategoria')
            db.session.commit()
            flash('Skladnik został edytowany!', category='success')
            return redirect('/admin')
        return render_template('editSkladnik.html', skladnik=skladnik)
    return redirect('/')


@admin.route('/edit/przepis/<int:id>', methods=['POST', 'GET'])
def editP(id):
    if current_user.is_authenticated:
        if db.session.query(Skladniki).count() >= 1:
            skladniki = db.session.query(Skladniki)
        else:
            skladniki = None
        przepis = Przepisy.query.filter_by(id=id).first()
        if request.method == 'POST':
            przepis.nazwa = request.form.get('nazwa')
            przepis.czas = request.form.get('czas')
            przepis.opis = request.form.get('opis')
            przepis.skladniki = request.form.get('skladniki')
            przepis.przepis = request.form.get('przepis')
            przepis.ListaSkladnikow = request.form.getlist('lista')
            przepis.ListaSkladnikow = " ".join(przepis.ListaSkladnikow)
            db.session.commit()
            przepis.grafika = request.files['grafika']
            grafika_name = przepis.grafika.filename
            if grafika_name != '':
                grafika_ext = os.path.splitext(grafika_name)[1]
                if grafika_ext in ['.png', '.jpg', '.jpeg', '.webp']:
                    grafika_name = grafika_name.replace(grafika_ext, '.png')
                    przepis.grafika.save(os.path.join('website/static/img', grafika_name))
                    db.session.add(przepis)
                    db.session.commit()
                    flash('Przepis został edytowany!', category='success')
                    return redirect('/admin')
                else:
                    flash('Nieprawidłowy format grafiki!', category='error')
                    return redirect(f'/admin/edit/przepis/{id}')
        return render_template('editPrzepis.html', przepis=przepis, skladniki=skladniki)
    return redirect('/')
