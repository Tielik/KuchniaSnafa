from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Przepisy(db.Model):
    # id przepisu 
    # nazwa przepisu
    # czas przygotowania
    # opis przepisu
    #zródło do zdjęcia
    #id składkików w stringu
    pass

class Skladniki(db.Model):
    pass
