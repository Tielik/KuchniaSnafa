from . import db
from flask_login import UserMixin

#function that delete row from database
def database_delete(row):
    db.session.delete(row)
    db.session.commit()
#function that add or update database
def database_commit(row):
    db.session.add(row)
    db.session.commit()

dish_ingredients = db.Table('dish_ingredients',
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)


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
#UPEWNIJ SIĘ BY NIE MOŻNA BYŁO POWTARZAĆ SKŁADNIKÓW DO DANIA!!!!!!!
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.String(100))
    description = db.Column(db.String(100))
    recipe = db.Column(db.String(1000))
    ingredients = db.relationship('Ingredient', secondary=dish_ingredients, backref='Dish')


'''
tabela skladniki
zawiera id, nazwa, kategoria
id- identyfikator skladnika
nazwa - nazwa skladnika
kategoria - kategoria skladnika
'''
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    category = db.Column(db.Integer)


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
