from flask import *

from database import *

farmer = Blueprint('farmer',__name__)

@farmer.route('/farmer_home')
def farmer_home():
    return render_template("farmer_home.html")


@farmer.route('/add_complaint', methods=['get', 'post'])
def add_complaint():
    data = {}

    # Fetch complaints in descending order (latest first)
    qry = "SELECT * FROM complaint ORDER BY date DESC"
    res = select(qry)
    if res:
        data['view'] = res

    if 'add' in request.form:
        complaint = request.form['complaint']
        print(complaint)

        y = "INSERT INTO complaint VALUES (NULL, '%s', '%s', 'pending', CURDATE())" % (session['fam'], complaint)
        insert(y)

        return "<script>alert('Successfully added'); window.location='add_complaint'</script>"

    return render_template("add_complaint.html", data=data)



@farmer.route('/about')
def farmer_about():
    return render_template("about.html")


@farmer.route('/service')
def farmer_service():
    return render_template("service.html")


from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

@farmer.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user session
    return redirect(url_for('public.login'))  # Redirect to login page


@farmer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authenticate user here
        session['user_id'] = user.id  # Set user session after successful login
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    return render_template('login.html')

