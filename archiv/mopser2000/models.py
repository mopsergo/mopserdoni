### models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Offer(db.Model):
    __tablename__ = 'Offers'
    id = db.Column(db.Integer, primary_key=True)
    anteilname = db.Column(db.String)
    verteilort = db.Column(db.String)
    anteilgr = db.Column(db.Float)
    gebotgruen = db.Column(db.Integer)
    gebotgelb = db.Column(db.Integer)
    gebotrot = db.Column(db.Integer)
    gebotackertage = db.Column(db.Integer)
    brot = db.Column(db.String)
    brot_anzahl = db.Column(db.Float)
    brot_kommentar = db.Column(db.String)
    name_a = db.Column(db.String)
    mail_a = db.Column(db.String)
    tel_a = db.Column(db.String)
    name_b = db.Column(db.String)
    mail_b = db.Column(db.String)
    name_c = db.Column(db.String)
    mail_c = db.Column(db.String)
    updated = db.Column(db.String)

    def __init__(self, anteilname, verteilort, anteilgr, gebotgruen, gebotgelb, gebotrot, gebotackertage, brot, brot_anzahl, brot_kommentar, name_a,mail_a,tel_a, name_b, mail_b, name_c, mail_c,  updated):
        self.anteilname = anteilname
        self.verteilort = verteilort
        self.anteilgr = anteilgr
        self.gebotgruen = gebotgruen
        self.gebotgelb = gebotgelb
        self.gebotrot = gebotrot
        self.gebotackertage = gebotackertage
        self.brot = brot
        self.brot_anzahl = brot_anzahl
        self.brot_kommentar = brot_kommentar
        self.name_a = name_a
        self.mail_a = mail_a
        self.tel_a = tel_a
        self.name_b = name_b
        self.mail_b = mail_b
        self.name_c = name_c
        self.mail_c = mail_c
        self.updated = updated

# table for needs

class Needs(db.Model):
    __tablename__ = 'Needs'
    id = db.Column(db.Integer, primary_key=True)
    solawiname = db.Column(db.String)
    saison = db.Column(db.String)
    anteile = db.Column(db.Integer)
    durchschnitt_gemuese = db.Column(db.Integer)
    durchschnitt_brot = db.Column(db.Integer)
    budget = db.Column(db.Integer)
    ackertage = db.Column(db.Integer)
    updated = db.Column(db.String)

    def __init__(self, solawiname, saison, anteile, durchschnitt_gemuese, durchschnitt_brot, budget, ackertage, updated):
        self.solawiname = solawiname
        self.saison = saison
        self.anteile = anteile
        self.durchschnitt_gemuese = durchschnitt_gemuese
        self.durchschnitt_brot = durchschnitt_brot
        self.budget = budget
        self.ackertage = ackertage
        self.updated = updated