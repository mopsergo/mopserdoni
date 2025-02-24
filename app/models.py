from . import db

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anteilname = db.Column(db.String(100))
    verteilort = db.Column(db.String(100))
    verteilort_wunsch = db.Column(db.String(100))
    anteilgr = db.Column(db.Float)
    gebotgruen = db.Column(db.Integer)
    gebotgelb = db.Column(db.Integer)
    gebotrot = db.Column(db.Integer)
    gebotackertage = db.Column(db.Integer)
    brot = db.Column(db.Float)
    #brot_anzahl = db.Column(db.Float)
    brot_kommentar = db.Column(db.String(255), nullable=True)
    name_a = db.Column(db.String(100))
    mail_a = db.Column(db.String(100))
    tel_a = db.Column(db.String(20))
    name_b = db.Column(db.String(100), nullable=True)
    mail_b = db.Column(db.String(100), nullable=True)
    name_c = db.Column(db.String(100), nullable=True)
    mail_c = db.Column(db.String(100), nullable=True)
    updated = db.Column(db.String)

    


class ProjectNeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    saison = db.Column(db.String(50))
    offers_needed = db.Column(db.Integer)
    avg_offer_veg = db.Column(db.Integer)
    avg_offer_bread = db.Column(db.Integer)
    avg_working_days = db.Column(db.Integer)
