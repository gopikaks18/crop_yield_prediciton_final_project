from flask import *

from public import public

from admin import admin

from farmer import farmer

from fertilizer import fertilizer

from notification import notification

from complaint import complaint

app = Flask(__name__)

app.secret_key='secretkey'

app.register_blueprint(public)

app.register_blueprint(admin)

app.register_blueprint(farmer)

app.register_blueprint(fertilizer)

app.register_blueprint(notification)

app.register_blueprint(complaint)

app.run(debug=True)
