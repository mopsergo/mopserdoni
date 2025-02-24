### app.py

import mailbox
from os import environ
import os
from unicodedata import name
from flask import Flask, render_template, request, flash, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
#from flask_basicauth import BasicAuth

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from io import BytesIO

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from datetime import date
import pandas as pd
import numpy as np
import xlsxwriter

from sqlalchemy import create_engine

###################
from flask import flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
##################


from models import db, Offer, Needs

from forms import AddRecord_Offer, AddRecord_Needs, DeleteForm_Offer, DeleteForm_Needs

app = Flask(__name__)
auth = HTTPBasicAuth()

#app.app_context()


##### Add Admin Users & Password for Mopser Analytics #####

users = {
    "fabi": generate_password_hash("control"),
    "admin": generate_password_hash("lookup")
}

### +++ EMAIL Config

gmail_user = 'leberheinz'
gmail_password = 'dzvnqggtcsinjpnn'


# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

# Flask-Bootstrap requires this line
Bootstrap(app)


# +++++++++++++++++++++++++++ DB SQLITE CONFIG ++++++++++++++++++++++++++++++++
basedir = os.path.abspath(os.path.dirname(__file__))
db_name = 'sqlite:///' + os.path.join(basedir, 'bietapp.db')

#db_name = 'sqlite:///bietapp.db'

app.config['SQLALCHEMY_DATABASE_URI'] = db_name
        
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
engine = create_engine(db_name)
db.init_app(app)
#db = SQLAlchemy(app)




# +++++++++++++++++++++++++++++++++++ DB MODELS ++++++++++++++++++++++++++++++++++++++

## models.py



# ++++++++++++++++++++++++++++++++++++++++++ FORMS ++++++++++++++++++++++++++++++++++

## forms.py



# +++++++++++++++++++++++
# get local date - does not account for time zone
# note: date was imported at top of script
def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    # build string in format 01-01-2000
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return date_string

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


# +++++++++++++++++++++++
# routes

@app.route('/')
def index():

    #df_needs = pd.read_sql_query("SELECT * FROM Needs;", raw_engine)

    df_needs = pd.read_sql_table(
	"Needs",  # table name
	con=engine
    )

    # df_o = [df_needs['anteile'][0],
     # #      df_needs['budget'][0],
      #      (df_needs['budget'][0]/12)/df_needs['anteile'][0],
         #   df_needs['ackertage'][0],
        #    df_needs['ackertage'][0]/df_needs['anteile'][0]]



    # df_o = [df_needs['solawiname'][0],
    #         df_needs['saison'][0],
    #         int(df_needs['anteile'][0]),
    #         int(df_needs['budget'][0]),
    #         int((df_needs['budget'][0]/12)/df_needs['anteile'][0]),
    #         df_needs['ackertage'][0],
    #         int(df_needs['ackertage'][0]/df_needs['anteile'][0])]


    df_o = [df_needs['solawiname'][0],
            df_needs['saison'][0],
            int(df_needs['anteile'][0]),
            int(df_needs['budget'][0]),
            int((df_needs['budget'][0]/12)/df_needs['anteile'][0]),
            df_needs['ackertage'][0],
            int(df_needs['ackertage'][0]/df_needs['anteile'][0])]

    #df_o = list(np.array(df_o).astype(int))


    return render_template('index.html', len= len(df_o), df_o=df_o)


# ++++++++++++++++++++++++++ ADD OFFER ++++++++++++++++++++++++++++

@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord_Offer()
    if form1.validate_on_submit():
        anteilname = request.form['anteilname']
        verteilort = request.form['verteilort']
        anteilgr = request.form['anteilgr']
        gebotgruen = request.form['gebotgruen']
        gebotgelb = request.form['gebotgelb']
        gebotrot = request.form['gebotrot']
        gebotackertage = request.form['gebotackertage']
        brot = request.form['brot']
        brot_anzahl = request.form['brot_anzahl']
        brot_kommentar = request.form['brot_kommentar']
        name_a = request.form['name_a']
        mail_a = request.form['mail_a']
        tel_a = request.form['tel_a']
        name_b = request.form['name_b']
        mail_b = request.form['mail_b']
        name_c = request.form['name_c']
        mail_c = request.form['mail_c']


        # get today's date from function, above all the routes
        updated = stringdate()
        # the data to be inserted into record model
        record = Offer(anteilname, verteilort, anteilgr, gebotgruen, gebotgelb, gebotrot, gebotackertage, brot, brot_anzahl, brot_kommentar, name_a, mail_a, tel_a, name_b, mail_b, name_c, mail_c, updated)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"""Dein Gebote für den Anteil {anteilname} wurden übermittelt.
        Notiere dir bitte, was du geboten hast. -> grün: {gebotgruen}€, gelb: {gebotgelb}€, rot: {gebotrot}€, Ackertage: {gebotackertage}.
        Brot {brot} und zwar {brot_anzahl}.
        """


# ++++++++++++++++++++ Write an EMAIL +++++++++++++++++++++++++++
 #            
        #message2 = f"grün: {gebotgruen}€, gelb: {gebotgelb}€, rot: {gebotrot}€, Ackertage: {gebotackertage}."
        sent_from = gmail_user
        to =  mail_a 
            #email_text = message.encode('utf-8')
        subject = 'Dein Gebot@MopserbietApp2000'
        email_message = f'Hallo {name_a},\n\ndeine Gebote für den Anteil {anteilname} sind eingetrudelt.\nDas hast du geboten: \ngrün: {gebotgruen}€, \ngelb: {gebotgelb}€, \nrot: {gebotrot}€, \nAckertage: {gebotackertage}\nBrot: {brot} und zwar {brot_anzahl}.\n\nSolidarische Grüße,\nMops'
        email_text = MIMEText(email_message.encode('utf-8'), 'plain', 'utf-8')


       # email_message = 'Hallo {name_a}, dein Gebote für den Anteil {anteilname} sind eingetrudelt. Das hast du geboten: grün: {gebotgruen}€, gelb: {gebotgelb}€, rot: {gebotrot}€, Ackertage: {gebotackertage}. Solidarische Grüße, Mops'
        #email_text = MIMEText(email_message.encode('utf-8'), 'plain', 'utf-8')
        email_text['Subject'] = Header(subject, 'utf-8')
        email_text['From'] = sent_from
        email_text['To'] = to

        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            #smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.sendmail(sent_from, to, email_text.as_string())
            smtp_server.close()
            print ("Email sent successfully!")
        except Exception as ex:
            print ("Something went wrong….",ex)

# +++++++++++++++++++++++++ END EMAIL BLOCK




        return render_template('add_record.html', message=message)
    else:
        # show validaton errors
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form1=form1)



#############################################################



# select a record to edit or delete
@app.route('/select_record')
@auth.login_required
def select_record():
    offers = Offer.query.order_by(Offer.anteilname).all()
    return render_template('select_record.html', offers=offers)


# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
@auth.login_required

def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    offer = Offer.query.filter(Offer.id == id).first()
    # two forms in this template
    #form1 = AddRecord_Offer_Round_start()
    form1= AddRecord_Offer()
    form2 = DeleteForm_Offer()
    return render_template('edit_or_delete.html', offer=offer, form1=form1, form2=form2, choice=choice)

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['POST'])
@auth.login_required
def delete_result():
    id = request.form['id_field']
    purpose = request.form['purpose']
    offer = Offer.query.filter(Offer.id == id).first()

    if purpose == 'delete':
        db.session.delete(offer)
        db.session.commit()
        message = f"Das Gebot von {offer.anteilname} wurde gelöscht."
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)


# result of edit - this function updates the record
@app.route('/edit_result', methods=['POST'])
@auth.login_required

def edit_result():
    id = request.form['id_field']
    # call up the record from the database
    gebot = Offer.query.filter(Offer.id == id).first()

    # update all values
    gebot.anteilname = request.form['anteilname']
    gebot.verteilort = request.form['verteilort']
    gebot.anteilgr = request.form['anteilgr']
    gebot.gebotgruen = request.form['gebotgruen']
    gebot.gebotgelb = request.form['gebotgelb']
    gebot.gebotrot = request.form['gebotrot']
    gebot.gebotackertage = request.form['gebotackertage']
    gebot.brot = request.form['brot']
    gebot.brot_anzahl = request.form['brot_anzahl']
    gebot.brot_kommentar = request.form['brot_kommentar']
    gebot.name_a = request.form['name_a']
    gebot.mail_a = request.form['mail_a']
    gebot.tel_a = request.form['tel_a']
    gebot.name_b = request.form['name_b']
    gebot.mail_b = request.form['mail_b']
    gebot.name_c = request.form['name_c']
    gebot.mail_c = request.form['mail_c']

    # get today's date from function, above all the routes
    gebot.updated = stringdate()

    form1 = AddRecord_Offer()
    if form1.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"Das Gebot von {gebot.anteilname} wurde geändert."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        gebot.id = id
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, gebot=gebot, choice='edit')


# ####### Delte all offers
@app.route('/delete_offers')
@auth.login_required
def delete_offers():
    return render_template('delete_offers.html')


# ####### really delete all offers
@app.route('/delete_all_offers')
@auth.login_required
def delete_all_offers():
    db.session.query(Offer).delete()
    db.session.commit()
    message = f"Alle Gebote wurden gelöscht."
    return render_template('result.html', message=message)
  


# ####### really delete all offers and bedarf
@app.route('/delete_all_offers_bedarf')
@auth.login_required
def delete_all_offers_bedarf():
    db.session.query(Offer).delete()
    db.session.query(Needs).delete()
    db.session.commit()
    message = f"Alles wurde gelöscht."
    return render_template('result.html', message=message)



# ++++++++++++++++++++++++++++++++++ MOPSER ANALYTICS ++++++++++++++++++++++++++++++++++++

# analyse app
@app.route('/html_list')
@auth.login_required
def html_list():
    offers = Offer.query.order_by(Offer.updated).all()
    return render_template('html_list.html', offers=offers)



@app.route('/analyse', methods=("POST", "GET"))
@auth.login_required
def analyse():

    df_gebote = pd.read_sql_table(
	"Offers",  # table name
	con=engine
    )


    df_needs = pd.read_sql_table(
	"Needs",  # table name
	con=engine
    )


    #gebote = Offer.query.all()
    #df_gebote = pd.DataFrame([t.__dict__ for t in gebote ])
    #df_gebote=df_gebote.drop(['_sa_instance_state'], axis=1)

    #bedarfe = Needs.query.all()
    #df_needs = pd.DataFrame([t.__dict__ for t in bedarfe ])
    #df_needs=df_needs.drop(['_sa_instance_state'], axis=1)


    df_analyse=pd.DataFrame({
        'Anteile':[df_needs['anteile'][0], df_gebote['anteilgr'].sum(), -(df_needs['anteile'][0]-df_gebote['anteilgr'].sum()),'-'],
        'gruen': [df_needs['budget'][0], df_gebote['gebotgruen'].sum()*12, -(df_needs['budget'][0]-df_gebote['gebotgruen'].sum()*12),-(df_needs['budget'][0]-df_gebote['gebotgruen'].sum()*12)/12],
        'gelb':[df_needs['budget'][0], df_gebote['gebotgelb'].sum()*12, -(df_needs['budget'][0]-df_gebote['gebotgelb'].sum()*12),  -(df_needs['budget'][0]-df_gebote['gebotgelb'].sum()*12)/12],
        'rot':[df_needs['budget'][0], df_gebote['gebotrot'].sum()*12, -(df_needs['budget'][0]-df_gebote['gebotrot'].sum()*12), -(df_needs['budget'][0]-df_gebote['gebotrot'].sum()*12)/12],
        'Ackertage':[df_needs['ackertage'][0], df_gebote['gebotackertage'].sum(),-(df_needs['ackertage'][0]-df_gebote['gebotackertage'].sum()),'0']
            }, index = ['Bedarf (Jahr)', 'Σ Gebote (Jahr)', 'Δ Jahr', 'Δ Monat'])

    df_analyse[['gruen','gelb','rot','Ackertage']]=df_analyse[['gruen','gelb','rot','Ackertage']].astype(int)
    df_analyse=df_analyse.replace({0:'-'})

    return render_template('analyse.html',  tables=[df_analyse.to_html(classes='table').replace('border="1" ', '').replace('class="dataframe table"','class="table"').replace('tr style="text-align: right;"','tr')], titles=df_analyse.columns.values)
    #return render_template('analyse.html',  tables=[df_analyse.to_html(classes='data')], titles=df_analyse.columns.values)


# ++++++++++++++++++++ DOWNLOAD OLD +++++++++++++++++++++++++++++++++++++++


@app.route("/download", methods=["GET"])
@auth.login_required
def download():
    
    df_gebote = pd.read_sql_table(
	"Offers",  # table name
	con=engine
    )

    #gebote = Offer.query.all()
    #df_gebote = pd.DataFrame([t.__dict__ for t in gebote ])
    #df_gebote=df_gebote.drop(['_sa_instance_state'], axis=1)

    df_gebote = df_gebote[[ 'id',
                            'anteilname',
                            'verteilort',
                            'anteilgr',
                            'gebotgruen',
                            'gebotgelb',
                            'gebotrot',
                            'gebotackertage',
                            'brot',
                            'brot_anzahl',
                            'brot_kommentar',
                            'name_a',
                            'mail_a',
                            'tel_a',
                            'name_b',
                            'mail_b',
                            'name_c',
                            'mail_c',
                            'updated']]


    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_gebote.to_excel(writer, sheet_name="Sheet1")

    output.seek(0)

    return send_file(output, attachment_filename="bietrunde.xlsx", as_attachment=True)


# ++++++++++++++++++++ DOWNLOAD NEW +++++++++++++++++++++++++++++++++++++++

from flask import make_response

@app.route("/download_new", methods=["GET"])
@auth.login_required
def download_new():
    
    df_gebote = pd.read_sql_table(
	"Offers",  # table name
	con=engine
    )

    #gebote = Offer.query.all()
    #df_gebote = pd.DataFrame([t.__dict__ for t in gebote ])
    #df_gebote=df_gebote.drop(['_sa_instance_state'], axis=1)

    df_gebote = df_gebote[[ 'id',
                            'anteilname',
                            'verteilort',
                            'anteilgr',
                            'gebotgruen',
                            'gebotgelb',
                            'gebotrot',
                            'gebotackertage',
                            'brot',
                            'brot_anzahl',
                            'brot_kommentar',
                            'name_a',
                            'mail_a',
                            'tel_a',
                            'name_b',
                            'mail_b',
                            'name_c',
                            'mail_c',
                            'updated']]


    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_gebote.to_excel(writer, sheet_name="Sheet1")

    output.seek(0)

    response = make_response(output.read())
    response.headers["Content-Disposition"] = "attachment; filename=bietrunde_donihof.xlsx"

    return response





#++++++++++++++++++++++ BEDARF +++++++++++++++++++++++++++++++++++#######

# add the need for the season 

@app.route('/add_bedarf', methods=['GET', 'POST'])
@auth.login_required

def add_bedarf():
    form3 = AddRecord_Needs()
    if form3.validate_on_submit():
        solawiname = request.form['solawiname']
        saison = request.form['saison']
        anteile = request.form['anteile']
        durchschnitt_gemuese = request.form['durchschnitt_gemuese']
        durchschnitt_brot = request.form['durchschnitt_brot']
        budget = request.form['budget']
        ackertage = request.form['ackertage']
    
        # get today's date from function, above all the routes
        updated = stringdate()
        # the data to be inserted into Record model
        record = Needs(solawiname, saison, anteile, durchschnitt_gemuese, durchschnitt_brot, budget, ackertage, updated)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"Der Bedarf wurde eingestellt"
        return render_template('add_bedarf.html', message=message)
    else:
        # show validaton errors
        for field, errors in form3.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form3, field).label.text,
                    error
                ), 'error')
        return render_template('add_bedarf.html', form3=form3)
       
# select a record to edit or delete
@app.route('/select_bedarf')
@auth.login_required

def select_bedarf():
    bedarfe = Needs.query.all()
    return render_template('select_bedarf.html', bedarfe=bedarfe)


# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete_bedarf', methods=['POST'])
@auth.login_required

def edit_or_delete_bedarf():
    id = request.form['id']
    choice = request.form['choice']
    bedarf = Needs.query.filter(Needs.id == id).first()
    # two forms in this template
    form3 = AddRecord_Needs()
    form4 = DeleteForm_Needs()
    return render_template('edit_or_delete_bedarf.html', bedarf=bedarf, form3=form3, form4=form4, choice=choice)




# result of delete - this function deletes the record
@app.route('/delete_bedarf', methods=['POST'])
@auth.login_required

def delete_bedarf():
    id = request.form['id_field']
    purpose = request.form['purpose']
    bedarf = Needs.query.filter(Needs.id == id).first()


    if purpose == 'delete':
        db.session.delete(bedarf)
        db.session.commit()
        message = f"Der Bedarf wurde gelöscht."
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)

# result of edit - this function updates the record
@app.route('/edit_bedarf', methods=['POST'])
@auth.login_required

def edit_bedarf():
    id = request.form['id_field']
    # call up the record from the database
    bedarf = Needs.query.filter(Needs.id == id).first()

    # update all values
    bedarf.solawiname = request.form['solawiname']
    bedarf.saison = request.form['saison']
    bedarf.anteile = request.form['anteile']
    bedarf.durchschnitt_gemuese = request.form['durchschnitt_gemuese']
    bedarf.durchschnitt_brot = request.form['durchschnitt_brot']
    bedarf.budget = request.form['budget']
    bedarf.ackertage = request.form['ackertage']
    # get today's date from function, above all the routes
    bedarf.updated = stringdate()

    form3 = AddRecord_Needs()
    if form3.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"Der Bedarf wurde geändert."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        bedarf.id = id
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form3.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form3, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete_bedarf.html', form3=form3, bedarf=bedarf, choice='edit')




################



# ####### starte
#@app.route('/starten')
#@auth.login_required
#def delete_offers():
 #   return render_template('delete_offers.html')


@app.route('/dbcreate')
@auth.login_required
def dbcreate():
    db.create_all()
    message = f"Datenbank wurde eingerichtet."
    return render_template('result.html', message=message)


# ####### initialise the app --> Database 
@app.route('/go')
@auth.login_required
def go():
    anteilname = '0'
    verteilort = '0'
    anteilgr = '0'
    gebotgruen = '0'
    gebotgelb = '0'
    gebotrot = '0'
    gebotackertage = '0'
    brot = '0'
    brot_anzahl= '0'
    brot_kommentar = '0'
    name_a = '0'
    mail_a = '0'
    tel_a = '0'
    name_b = '0'
    mail_b = '0'
    name_c = '0'
    mail_c = '0'

        # get today's date from function, above all the routes
    updated = stringdate()
        # the data to be inserted into record model
    start_offer = Offer(anteilname, verteilort, anteilgr, gebotgruen, gebotgelb, gebotrot, gebotackertage, brot, brot_anzahl, brot_kommentar, name_a, mail_a, tel_a, name_b, mail_b, name_c, mail_c, updated)
    #start_offer = Offer(runde, anteilname, anteilgr, gebot, name, mail, tel, adresse, geburtsdatum, updated)
    # Flask-SQLAlchemy magic adds record to database
    db.session.add(start_offer)

    solawiname = 'BLABLABLA'
    saison = '00/00'
    anteile = '1'
    durchschnitt_gemuese = '1'
    durchschnitt_brot = '1'
    budget = '1'
    ackertage = '1'
    
        # the data to be inserted into Record model
    start_need = Needs(solawiname, saison, anteile, durchschnitt_gemuese, durchschnitt_brot, budget, ackertage, updated)
        # Flask-SQLAlchemy magic adds record to database
    db.session.add(start_need)
    db.session.commit()
        # create a message to send to the template

    message = f"Mopser-Biet-App erfolgreich initialisiert."
    return render_template('result.html', message=message)
  


# +++++++++++++++++++++++
# error routes
# https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/#registering-an-error-handler

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', pagetitle="404 Error - Page Not Found", pageheading="Page not found (Error 404)", error=e), 404

@app.errorhandler(405)
def form_not_posted(e):
    return render_template('error.html', pagetitle="405 Error - Form Not Submitted", pageheading="The form was not submitted (Error 405)", error=e), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', pagetitle="500 Error - Internal Server Error", pageheading="Internal server error (500)", error=e), 500

# +++++++++++++++++++++

if __name__ == "__main__":
  app.run()