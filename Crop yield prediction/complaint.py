from flask import *

from database import *

complaint = Blueprint('complaint',__name__)

@complaint.route('/complaint_home')
def complaint_home():
    return render_template("complaint_home.html")

