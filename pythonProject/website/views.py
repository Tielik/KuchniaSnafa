from flask import Blueprint, render_template, request, flash, json, jsonify
# from flask_login import login_required, logout_user, current_user
#
# from . import db
# from .models import Note


views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form != None:
        f = request.form
        for key in f:
            for value in f.getlist(key):
                print(key,":", value)
        return render_template('index.html', form = f)
    return render_template('index.html')

@views.route('/admin')
def admin():
    return render_template('admin.html')