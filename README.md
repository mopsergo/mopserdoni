
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── user.py
│   ├── admin.py
│   ├── templates/
│       ├── layout.html
│       ├── user_form.html
│       ├── admin.html
├── run.py
├── .env


admin
lookylook


------------

## run localy with rye
* Im Projektordner
rye pin 3
rye init
rye add mailbox flask flask_sqlalchemy flask_bootstrap flask_httpauth flask_wtf pandas numpy xlsxwriter datetime python-dotenv email-validator

rye sync

### Flask Migrate Setup
* rye run flask db init
* rye run flask db migrate -m "Initial migration."
* rye run flask db upgrade

Migrate
* rye run flask db migrate -m "Add new column to ModelName"
* rye run flask db migrate -m "Add offers_needed column to ProjectNeed"


* rye run flask run



## pythonanywhere
* zip -> app
* upload app.zip and .env
* unzip app.zip
* wsgi file anpassen