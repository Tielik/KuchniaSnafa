from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

'''
tabela przepisy
zawiera id, nazwa, czas, opis, skladniki, przepis
id- identyfikator przepisu
nazwa - nazwa przepisu
czas - czas trwania przepisu
opis - opis przepisu
przepis - tresc przepisu
Listaskladnikow - składniki przepisu (zapisywane w formie liczbowej)
'''
class Przepisy(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nazwa = db.Column(db.String(100))
    czas = db.Column(db.String(100))
    opis = db.Column(db.String(100))
    przepis = db.Column(db.String(1000))
    ListaSkladnikow = db.Column(db.String(100))

'''
tabela skladniki
zawiera id, nazwa, kategoria
id- identyfikator skladnika
nazwa - nazwa skladnika
kategoria - kategoria skladnika
'''
class Skladniki(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Nazwa = db.Column(db.String(100))
    kategoria = db.Column(db.Integer)


'''
tabela admin
zawiera id, hasło, imie
id- identyfikator admina
hasło - hasło admina
imie - imie admina
'''
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
