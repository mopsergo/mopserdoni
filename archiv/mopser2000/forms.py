### forms.py


from flask_wtf import FlaskForm
from wtforms import (HiddenField, StringField, SelectField, IntegerField, 
                    SubmitField)
from wtforms.validators import (InputRequired, Length, NumberRange)

# ++++++++++++++++++++++++++++++++++++++++++ OFFERS ++++++++++++++++++++++++++++++++++
# forms with Flask-WTF

# form for add_record and edit_or_delete
# each field includes validation requirements and messages
class AddRecord_Offer(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    anteilname = StringField('Name des Anteils (denk dir einen aus!)', [ InputRequired(),
        #Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid name"),
        #Length(min=3, max=30, message="Invalid name name length") ])
        Length(min=3, max=25, message="Ungültige Namenslänge")])

    verteilort = SelectField('Wo holst du dein Gemüse?', [ InputRequired()],
        choices=[ ('', ''), ('Westend', 'Westend'),
        ('Mammendorf', 'Mammendorf'), ('anderer', 'anderer'), ])

    anteilgr = SelectField('Wähle die Größe deines Anteils:', [ InputRequired()],
        choices=[ ('1', '1'), ('0.5', '0.5'),
        ('1.5', '1.5'), ])

    gebotgruen = IntegerField('grün: Das zahle ich locker!', [ InputRequired(),
        # NumberRange(min=1, max=999, message="Invalid range") ])
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])

    gebotgelb = IntegerField('gelb: Das wäre auch in Ordnung!', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])

    gebotrot = IntegerField('rot: Das ist meine Schmerzgrenze!', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])

    gebotackertage = IntegerField('Wie viele Tage willst du (dein Anteil) kommende Saison ackern?', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])

    #brot = BooleanField('Brot Anzahl', [InputRequired()])  # This is your checkbox field
    brot = SelectField('Du Brot?', [ InputRequired()],
        choices=[ ('nein', 'nein'),('wöchentlich', 'wöchentlich'),('2-wöchentlich', '2-wöchentlich'),
        ('1 mal im Monat', '1 mal im Monat'), ('ab und zu', 'ab und zu')])

    brot_anzahl = SelectField('Wie viel Brot?', [ InputRequired()],
        choices=[('0', '0'), ('0.25', '1/4'),('0.5', '1/2'),('1', '1'),
        ('1.5', '1 1/2'), ('2', '2'), ('100', '∞') ])

    brot_kommentar = StringField('(optional) Kommentar zum Brot (z.B. Dinkel, kein Roggen, nur Vollkorn usw.)')

    name_a = StringField('Name einer verantwortlichen Person für deinen Anteil', [ InputRequired(),
        Length(min=3, max=30, message="Ungültige Namenslänge") ])
    
    mail_a = StringField('E-Mail einer verantwortlichen Person für deinen Anteil', [ InputRequired(),
        Length(min=3, max=30, message="Ungültige Namenslänge") ])
    
    tel_a = StringField('Telefonnummer einer verantwortlichen Person für deinen Anteil', [ InputRequired(),
        Length(min=3, max=30, message="Ungültige Namenslänge") ])


    name_b = StringField('(optional) Name einer weiteren Person für deinen Anteil')
    
    mail_b = StringField('(optional) E-Mail einer weiteren Person für deinen Anteil')
    
    name_c = StringField('(optional) Name einer weiteren Person für deinen Anteil')
    
    mail_c = StringField('(optional) E-Mail einer weiteren Person für deinen Anteil')


   # price = FloatField('Retail price per pair', [ InputRequired(),
    #    NumberRange(min=1.00, max=99.99, message="Invalid range")
     #   ])
    # updated - date - handled in the route
    updated = HiddenField()
    submit = SubmitField('Abschicken')


################ NEEDS #############

# form for add bedarf
# each field includes validation requirements and messages
class AddRecord_Needs(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    
    solawiname = StringField('Name deiner Solawi à la Solawi Donihof', [ InputRequired(),
        Length(min=3, max=80, message="Ungültige Namenslänge")])
    
    saison = StringField('Saison à la 22/23', [ InputRequired(),
        Length(min=3, max=30, message="Ungültige Namenslänge")])

    anteile = IntegerField('Anzahl der Anteile', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])

    durchschnitt_gemuese = IntegerField('Durchschnitt Gemüse / Anteil', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])

    durchschnitt_brot =  IntegerField('Durchschnitt Brot / Anteil', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")])
        
    budget = IntegerField('Jahresbudget', [ InputRequired(),
        NumberRange(min=1, max=9999999, message="Ungültiger Bereich")
        ])
    ackertage = IntegerField('Benötigte Ackertage', [ InputRequired(),
        NumberRange(min=1, max=999, message="Ungültiger Bereich")
        ])
    # updated - date - handled in the route
    updated = HiddenField()
    submit = SubmitField('Bedarf hinzufügen')


# small form
class DeleteForm_Offer(FlaskForm):
    id_field = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Gebot löschen')

class DeleteForm_Needs(FlaskForm):
    id_field = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Bedarf löschen')
