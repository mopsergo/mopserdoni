from flask import Blueprint, render_template, request, flash, send_file, abort
from io import BytesIO
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from werkzeug.security import check_password_hash
from .models import db, Offer, Needs
from .forms import AddRecord_Offer, AddRecord_Needs, DeleteForm_Offer, DeleteForm_Needs
from . import auth

import os
from sqlalchemy import create_engine
from datetime import date

main_app = Blueprint('main_app', __name__)

gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = 'sqlite:///' + os.path.join(basedir, 'bietapp.db')
engine = create_engine(db_name)

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return date_string

@main_app.route('/')
def index():
    df_needs = pd.read_sql_table("Needs", con=engine)
    df_o = [
        df_needs['solawiname'][0],
        df_needs['saison'][0],
        int(df_needs['anteile'][0]),
        int(df_needs['budget'][0]),
        int((df_needs['budget'][0]/12)/df_needs['anteile'][0]),
        df_needs['ackertage'][0],
        int(df_needs['ackertage'][0]/df_needs['anteile'][0])
    ]
    return render_template('index.html', len=len(df_o), df_o=df_o)

@main_app.route('/add_record', methods=['GET', 'POST'])
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
        updated = stringdate()
        record = Offer(
            anteilname, verteilort, anteilgr, gebotgruen, gebotgelb, gebotrot, gebotackertage,
            brot, brot_anzahl, brot_kommentar, name_a, mail_a, tel_a, name_b, mail_b, name_c, mail_c, updated
        )
        db.session.add(record)
        db.session.commit()
        message = f"Dein Gebote für den Anteil {anteilname} wurden übermittelt."
        
        # Email sending
        sent_from = gmail_user
        to = mail_a
        subject = 'Dein Gebot@MopserbietApp2000'
        email_message = f'Hallo {name_a},\n\ndeine Gebote für den Anteil {anteilname}...'
        email_text = MIMEText(email_message.encode('utf-8'), 'plain', 'utf-8')
        email_text['Subject'] = Header(subject, 'utf-8')
        email_text['From'] = sent_from
        email_text['To'] = to

        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, email_text.as_string())
            smtp_server.close()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong…", ex)

        return render_template('add_record.html', message=message)
    else:
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form1=form1)

# More routes as needed...

