from flask import Blueprint, render_template, redirect, url_for, flash, request

from .forms import OfferForm
from .models import Offer, ProjectNeed
from . import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from datetime import date

gmail_user = 'leberheinz'
gmail_password = 'dzvnqggtcsinjpnn'


user_bp = Blueprint('user', __name__)

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    # build string in format 01-01-2000
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return date_string

@user_bp.route('/')
def index():
    project_need = ProjectNeed.query.first()
    return render_template('index.html', project_need=project_need)


@user_bp.route('/submit_offer', methods=['GET', 'POST'])
def submit_offer():
    form = OfferForm()
    project_need = ProjectNeed.query.first()
    
    if request.method == 'POST':  # Check if the request is a POST
        if form.validate_on_submit():
            offer = Offer(
                anteilname=form.anteilname.data,
                verteilort=form.verteilort.data,
                verteilort_wunsch=form.verteilort_wunsch.data,
                anteilgr=form.anteilgr.data,
                gebotgruen=form.gebotgruen.data,
                gebotgelb=form.gebotgelb.data,
                gebotrot=form.gebotrot.data,
                gebotackertage=form.gebotackertage.data,
                brot=form.brot.data,
                #brot_anzahl=form.brot_anzahl.data,
                brot_kommentar=form.brot_kommentar.data,
                name_a=form.name_a.data,
                mail_a=form.mail_a.data,
                tel_a=form.tel_a.data,
                name_b=form.name_b.data,
                mail_b=form.mail_b.data,
                name_c=form.name_c.data,
                mail_c=form.mail_c.data,
                updated=stringdate()
            )
            db.session.add(offer)
            db.session.commit()

            message = f'Hallo {offer.name_a},\n\ndeine Gebote für den Anteil {offer.anteilname} sind eingetrudelt.\n\n Du hast für {offer.anteilgr} Gemüseanteil(e) und {offer.brot} Brotanteil(e) geboten:\ngrün: {offer.gebotgruen} €, \ngelb: {offer.gebotgelb} €, \nrot: {offer.gebotrot} €, \nAckertage: {offer.gebotackertage}\n\n\nSolidarische Grüße,\nMops*'
            
            flash(message, 'success')

            # ++++++++++++++++++++ Write an EMAIL +++++++++++++++++++++++++++
            sent_from = gmail_user
            to = offer.mail_a 
            subject = 'Dein Gebot@MopserbietApp3000'
            email_message = message
            email_text = MIMEText(email_message.encode('utf-8'), 'plain', 'utf-8')

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
                print("Email sent successfully!")
            except Exception as ex:
                print("Something went wrong….", ex)

            return redirect(url_for('user.index'))
        else:
            # Flash an error message if form validation fails during POST
            flash('Falsche Eingaben. Bitte überprüfe deine Eingaben und versuche es erneut. Achte darauf eine korrekte E-Mail Adresse anzugeben.', 'success')

    return render_template('user_form.html', form=form, project_need=project_need)
