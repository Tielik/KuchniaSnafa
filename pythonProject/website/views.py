from flask import Blueprint, render_template, request, flash, json, jsonify
from flask_login import login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Admin  #Skladniki Przepisy

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form != None:
        f = request.form
        for key in f:
            for value in f.getlist(key):
                print(key, ":", value)
        return render_template('index.html', form=f)
    return render_template('index.html')
#PASY Admin h:1234

@views.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        name = request.form.get('Admin')
        password = request.form.get('password')
        print(db.session.query(db.exists().where(Admin.name == name)).scalar())
        if db.session.query(db.exists().where(Admin.name == name)).scalar():
            user = Admin.query.filter_by(name=name).first()
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                return render_template('admin.html')
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template('Login.html')
        else:
            flash('Name does not exist.', category='error')
            return render_template('Login.html')

    else:
        return render_template('Login.html')
