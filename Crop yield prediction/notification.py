from flask import *

from database import *

notification = Blueprint('notification',__name__)

@notification.route('/notification_home')
def notification_home():
    return render_template("notification_home.html")

