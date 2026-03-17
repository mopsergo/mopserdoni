from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file,make_response
from flask_wtf.csrf import generate_csrf
from .forms import ProjectNeedForm, OfferForm
from .models import Offer, ProjectNeed
from . import db, auth
import pandas as pd
from io import BytesIO
import os
from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__)

users = {
    "fabi": generate_password_hash("control"),
    "admin": generate_password_hash("lookup")
}

@auth.verify_password
def verify_password(username, password):
    #return username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD')

    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@admin_bp.route('/', methods=['GET'])
@auth.login_required
def admin_dashboard():
    #project_needs = ProjectNeed.query.all()
    project_need = ProjectNeed.query.first()

    offers = Offer.query.all()
    
    # Calculate statistics
    total_offers = len(offers)
    total_veg_sum = sum(offer.anteilgr for offer in offers)
    total_bread_sum = sum(offer.brot for offer in offers)
    sum_offers = f'G: {total_veg_sum} / B: {total_bread_sum}'

    # dynamic_bread_costs = total_bread_sum * project_need.avg_offer_bread
    # dynamic_veg_costs = total_veg_sum * project_need.avg_offer_veg
    # total_dynamic_costs = dynamic_bread_costs + dynamic_veg_costs

    dynamic_bread_costs_year = total_bread_sum * project_need.avg_offer_bread * 12
    dynamic_veg_costs_year = total_veg_sum * project_need.avg_offer_veg * 12
    total_dynamic_costs_year = dynamic_bread_costs_year+dynamic_veg_costs_year
    total_dynamic_working_days_year = total_veg_sum*project_need.avg_working_days


    # Calculate totals month
    
    # Calculate totals year
    total_working_days_year = sum(offer.gebotackertage for offer in offers)
    total_offers_green_year = sum(offer.gebotgruen for offer in offers) * 12
    total_offers_yellow_year = sum(offer.gebotgelb for offer in offers) * 12
    total_offers_red_year = sum(offer.gebotrot for offer in offers) * 12

    # Diffefences year
    diff_offers_green_year = total_offers_green_year - total_dynamic_costs_year
    diff_offers_yellow_year = total_offers_yellow_year - total_dynamic_costs_year
    diff_offers_red_year = total_offers_red_year - total_dynamic_costs_year
    diff_working_days_year = total_working_days_year - total_dynamic_working_days_year

    # Calculate normalized averages
    valid_offers = [o for o in offers if o.anteilgr]

    avg_offer_green_normalized = (
        sum(o.gebotgruen / o.anteilgr for o in valid_offers) / len(valid_offers)
        if valid_offers else 0
    )

    avg_offer_yellow_normalized = (
        sum(o.gebotgelb / o.anteilgr for o in valid_offers) / len(valid_offers)
        if valid_offers else 0
    )

    avg_offer_red_normalized = (
        sum(o.gebotrot / o.anteilgr for o in valid_offers) / len(valid_offers)
        if valid_offers else 0
    )

    avg_working_days_normalized = (
        sum(o.gebotackertage / o.anteilgr for o in valid_offers) / len(valid_offers)
        if valid_offers else 0
    )

    # avg_offer_green_normalized = sum(offer.gebotgruen / offer.anteilgr if offer.anteilgr else 0 for offer in offers) / total_offers if total_offers else 0
    # avg_offer_yellow_normalized = sum(offer.gebotgelb / offer.anteilgr if offer.anteilgr else 0 for offer in offers) / total_offers if total_offers else 0
    # avg_offer_red_normalized = sum(offer.gebotrot / offer.anteilgr if offer.anteilgr else 0 for offer in offers) / total_offers if total_offers else 0
    # avg_working_days_normalized = sum(offer.gebotackertage / offer.anteilgr if offer.anteilgr else 0 for offer in offers) / total_offers if total_offers else 0
    # #avg_offer_green_normalized = sum(offer.gebotgruen / offer.anteilgr for offer in offers) / total_veg_sum if total_veg_sum else 0
    #avg_offer_yellow_normalized = sum(offer.gebotgelb / offer.anteilgr for offer in offers) / total_veg_sum if total_veg_sum else 0
    #avg_offer_red_normalized = sum(offer.gebotrot / offer.anteilgr for offer in offers) / total_veg_sum if total_veg_sum else 0
    #avg_working_days_normalized = sum(offer.gebotackertage / offer.anteilgr for offer in offers) / total_veg_sum if total_veg_sum else 0



    csrf_token = generate_csrf()  # Generate CSRF token



    return render_template(
        'admin.html',
        #project_needs=project_needs,
        project_need = project_need,
        dynamic_veg_costs_year = dynamic_veg_costs_year,
        dynamic_bread_costs_year = dynamic_bread_costs_year,
         total_dynamic_costs_year= total_dynamic_costs_year,
         total_dynamic_working_days_year=total_dynamic_working_days_year,
         avg_offer_green_normalized = round(avg_offer_green_normalized),
         avg_offer_yellow_normalized = round(avg_offer_yellow_normalized),
         avg_offer_red_normalized = round(avg_offer_red_normalized),
         avg_working_days_normalized=round(avg_working_days_normalized),
         sum_offers = sum_offers,
         total_offers_green_year = total_offers_green_year,
         total_offers_yellow_year = total_offers_yellow_year,
         total_offers_red_year = total_offers_red_year,
         total_working_days_year = total_working_days_year,
         diff_offers_green_year = diff_offers_green_year,
         diff_offers_yellow_year = diff_offers_yellow_year,
         diff_offers_red_year = diff_offers_red_year,
         diff_working_days_year = diff_working_days_year,
         ##
         csrf_token=csrf_token)

@admin_bp.route('/project_need', methods=['GET', 'POST'])
@auth.login_required
def manage_project_need():
    project_need = ProjectNeed.query.first()  # Get the single ProjectNeed
    if not project_need:
        flash("Nix gefunden!", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    form = ProjectNeedForm(obj=project_need)
    if form.validate_on_submit():
        form.populate_obj(project_need)
        db.session.commit()
        flash('Bedarf geändert!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('edit_project_need.html', form=form)


@admin_bp.route('/offers', methods=['GET'])
@auth.login_required
def view_offers():
    offers = Offer.query.all()
    csrf_token = generate_csrf()  # Generate CSRF token
    return render_template('view_offers.html', offers=offers, csrf_token=csrf_token)

@admin_bp.route('/offer/<int:offer_id>', methods=['GET'])
@auth.login_required
def offer_details(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    return render_template('offer_details.html', offer=offer)

@admin_bp.route('/edit/<int:offer_id>', methods=['GET', 'POST'])
@auth.login_required
def edit_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    #form = OfferForm()
    form = OfferForm(obj=offer)

    if request.method == 'POST':
        # Update offer details based on form submission
        offer.anteilname = request.form['anteilname']
        offer.verteilort = request.form['verteilort']
        offer.verteilort_wunsch=request.form['verteilort_wunsch']
        offer.anteilgr = float(request.form['anteilgr'])
        offer.gebotgruen = int(request.form['gebotgruen'])
        offer.gebotgelb = int(request.form['gebotgelb'])
        offer.gebotrot = int(request.form['gebotrot'])
        offer.gebotackertage = int(request.form['gebotackertage'])
        offer.brot = float(request.form['brot'])
        #offer.brot_anzahl = float(request.form['brot_anzahl'])
        offer.brot_kommentar = request.form.get('brot_kommentar', '')
        offer.name_a = request.form['name_a']
        offer.mail_a = request.form['mail_a']
        offer.tel_a = request.form['tel_a']
        offer.name_b = request.form.get('name_b', '')
        offer.mail_b = request.form.get('mail_b', '')
        offer.name_c = request.form.get('name_c', '')
        offer.mail_c = request.form.get('mail_c', '')
        
        db.session.commit()
        flash(f'Gebot {offer.anteilname} geändert.', 'success')
        return redirect(url_for('admin.view_offers', offer_id=offer.id))

    return render_template('edit_offer.html', offer=offer, form=form)

@admin_bp.route('/delete/<int:offer_id>', methods=['POST'])
@auth.login_required
def delete_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    flash('Gelöscht!', 'success')
    return redirect(url_for('admin.view_offers'))

@admin_bp.route('/download', methods=['GET'])
@auth.login_required
def download_offers():
    offers = Offer.query.all()
    data = [{
        'Anteilname': offer.anteilname,
        'Verteilort': offer.verteilort,
        'Wunschort': offer.verteilort_wunsch,
        'Anteilgröße': offer.anteilgr,
        'Gebot Grün': offer.gebotgruen,
        'Gebot Gelb': offer.gebotgelb,
        'Gebot Rot': offer.gebotrot,
        'Gebot Ackertage': offer.gebotackertage,
        'Brot': offer.brot,
        'Brot Kommentar': offer.brot_kommentar,
        #'Brot Anzahl': offer.brot_anzahl,
        'Name A': offer.name_a,
        'Mail A': offer.mail_a,
        'Tel A': offer.tel_a,
        'Name B': offer.name_b,
        'Mail B': offer.mail_b,
        'Name C': offer.name_c,
        'Mail C': offer.mail_c,
        'Datum': offer.updated
    } for offer in offers]
    
    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1")

    output.seek(0)

    response = make_response(output.read())
    response.headers["Content-Disposition"] = "attachment; filename=bietrunde_donihof.xlsx"

    return response

@admin_bp.route('/reset', methods=['POST'])
@auth.login_required
def reset_app():
    db.session.query(Offer).delete()
    db.session.commit()
   #csrf_token = generate_csrf()  # Generate CSRF token

    flash('Alles wurde gelöscht!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

