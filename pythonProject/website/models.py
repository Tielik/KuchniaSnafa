from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Przepisy(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nazwa = db.Column(db.String(100))
    czas = db.Column(db.String(100))
    opis = db.Column(db.String(100))
    skladniki = db.Column(db.String(100))
    przepis = db.Column(db.String(1000))
    ListaSkladnikow = db.Column(db.String(50))

class Skladniki(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Nazwa = db.Column(db.String(100))
    kategoria = db.Column(db.Integer)



class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
