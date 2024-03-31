from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Przepisy(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # nazwa przepisu
    # czas przygotowania
    # opis przepisu
    # zródło do zdjęcia
    # id składkików w stringu
    pass


class Skladniki(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)



class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
