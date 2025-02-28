from flask import *

from database import *

fertilizer = Blueprint('fertilizer',__name__)

@fertilizer.route('/fertilizer_home')
def fertilizer_home():
    return render_template("fertilizer_home.html")

