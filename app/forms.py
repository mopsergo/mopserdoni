from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Optional,InputRequired
#from wtforms.validators import ValidationError

class OfferForm(FlaskForm):
    anteilname = StringField('Ein Name für deinen Anteil (Denk Dir einen aus!)', validators=[DataRequired()])
    verteilort = SelectField('Wo holst du dein Gemüse und ggf. Brot ab?', choices=[ ('Westend', 'Westend'), ('Mammendorf', 'Mammendorf')], validators=[DataRequired()])
    verteilort_wunsch = StringField('(optional) Wenn möglich, würde ich gerne an einem anderen Ort abholen (wird auf der MV besprochen und entschieden):', validators=[Optional()])
    anteilgr = SelectField('Ein, halber oder mehr Gemüseanteil(e)?', choices=[(1, '1 Gemüseanteil'), (0.5, '1/2 Gemüseanteil'), (2, '2 Gemüseanteile'), (3, '3 Gemüseanteile')], coerce=float, validators=[DataRequired()])
    brot = SelectField('Kein, halber, ein oder mehr Brotanteil(e)?', choices=[(0, 'Kein Brotanteil'), (0.5, '1/2 Brotanteil'), (1, '1 Brotanteil'), (2, '2 Brotanteile'),(3, '3 Brotanteile')], coerce=float, validators=[InputRequired()])
    #brot_anzahl = FloatField('Brot Anzahl', validators=[DataRequired()])
    #brot_anzahl= SelectField('Wie viel Brot willst du?', choices=[(0, 'Keins'), (1, 'Eins (1kg)'), (0.5, 'Halb (500g)'), (2, 'Zwei/1 Großes (2kg)'), (3, 'Drei oder so')], coerce=float, validators=[InputRequired()])
    brot_kommentar = TextAreaField('(optional) Was hast du zum Brot zu sagen, zB. nur Dinkel, kein Vollkorn, alle 2 Wochen etc?', validators=[Optional()])
    gebotgruen = IntegerField('grün: Das zahle ich locker!', validators=[DataRequired()])
    gebotgelb = IntegerField('gelb: Das wäre auch in Ordnung!', validators=[DataRequired()])
    gebotrot = IntegerField('rot: Das ist meine Schmerzgrenze!', validators=[DataRequired()])
    gebotackertage = IntegerField('Wie viele Tage willst du (dein Anteil) kommende Saison ackern? ', validators=[InputRequired()])
    name_a = StringField('Name einer verantwortlichen Person für deinen Anteil', validators=[DataRequired()])
    mail_a = StringField('E-Mail einer verantwortlichen Person für deinen Anteil', validators=[Email(), DataRequired()])
    tel_a = StringField('Telefonnummer einer verantwortlichen Person für deinen Anteil', validators=[DataRequired()])
    name_b = StringField('(optional) Name einer weiteren Person für deinen Anteil', validators=[Optional()])
    mail_b = StringField('(optional) E-Mail einer weiteren Person für deinen Anteil', validators=[Optional(), Email()])
    name_c = StringField('(optional) Name einer weiteren Person für deinen Anteil', validators=[Optional()])
    mail_c = StringField('(optional) E-Mail einer weiteren Person für deinen Anteil ', validators=[Optional(), Email()])
    updated = HiddenField()

    submit = SubmitField('Abschicken')

class ProjectNeedForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    saison = StringField('Saison', validators=[DataRequired()])
    offers_needed = FloatField('Angestrebte Anzahl an Anteilen', validators=[DataRequired()])
    avg_offer_veg = FloatField('Durchschnittliches Angebot für Gemüse', validators=[DataRequired()])
    avg_offer_bread = FloatField('Durchschnittliches Angebot für Brot', validators=[DataRequired()])
    avg_working_days = IntegerField('Durchschnittliche Arbeitstage', validators=[DataRequired()])
