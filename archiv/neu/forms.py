from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange

class AddRecord_Offer(FlaskForm):
    id_field = HiddenField()
    anteilname = StringField('Name des Anteils (denk dir einen aus!)', [InputRequired(), Length(min=3, max=25)])
    verteilort = SelectField('Wo holst du dein Gemüse?', [InputRequired()], choices=[('', ''), ('Westend', 'Westend'), ('Mammendorf', 'Mammendorf'), ('anderer', 'anderer')])
    anteilgr = SelectField('Wähle die Größe deines Anteils:', [InputRequired()], choices=[('1', '1'), ('0.5', '0.5'), ('1.5', '1.5')])
    gebotgruen = IntegerField('grün: Das zahle ich locker!', [InputRequired(), NumberRange(min=1, max=999)])
    gebotgelb = IntegerField('gelb: Das wäre auch in Ordnung!', [InputRequired(), NumberRange(min=1, max=999)])
    gebotrot = IntegerField('rot: Das ist meine Schmerzgrenze!', [InputRequired(), NumberRange(min=1, max=999)])
    gebotackertage = IntegerField('Wie viele Tage willst du (dein Anteil) kommende Saison ackern?', [InputRequired(), NumberRange(min=1, max=999)])
    brot = SelectField('Du Brot?', [InputRequired()], choices=[('nein', 'nein'), ('wöchentlich', 'wöchentlich'), ('2-Wöchig', '2-Wöchig'), ('1 mal im Monat', '1 mal im Monat'), ('ab und zu', 'ab und zu')])
    brot_anzahl = SelectField('Wie viel Brot?', [InputRequired()], choices=[('0.25', '1/4'), ('0.5', '1/2'), ('1', '1'), ('1.5', '1 1/2')])
    brot_kommentar = StringField('Kommentar zum Brot')
    name_a = StringField('Name einer verantwortlichen Person für deinen Anteil', [InputRequired(), Length(min=3, max=30)])
    mail_a = StringField('E-Mail einer verantwortlichen Person für deinen Anteil', [InputRequired(), Length(min=3, max=30)])
    tel_a = StringField('Telefonnummer einer verantwortlichen Person für deinen Anteil', [InputRequired(), Length(min=3, max=30)])
    name_b = StringField('(optional) Name einer weiteren Person für deinen Anteil')
    mail_b = StringField('(optional) E-Mail einer weiteren Person für deinen Anteil')
    name_c = StringField('(optional) Name einer weiteren Person für deinen Anteil')
    mail_c = StringField('(optional) E-Mail einer weiteren Person für deinen Anteil')
    updated = HiddenField()
    submit = SubmitField('Abschicken')

class AddRecord_Needs(FlaskForm):
    id_field = HiddenField()
    solawiname = StringField('Name deiner Solawi à la Solawi Donihof', [InputRequired(), Length(min=3, max=80)])
    saison = StringField('Saison à la 22/23', [InputRequired(), Length(min=3, max=30)])
    anteile = IntegerField('Anzahl der Anteile', [InputRequired(), NumberRange(min=1, max=999)])
    budget = IntegerField('Jahresbudget', [InputRequired(), NumberRange(min=1, max=9999999)])
    ackertage = IntegerField('Benötigte Ackertage', [InputRequired(), NumberRange(min=1, max=999)])
    updated = HiddenField()
    submit = SubmitField('Bedarf hinzufügen')

class DeleteForm_Offer(FlaskForm):
    id_field = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Gebot löschen')

class DeleteForm_Needs(FlaskForm):
    id_field = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Bedarf löschen')
