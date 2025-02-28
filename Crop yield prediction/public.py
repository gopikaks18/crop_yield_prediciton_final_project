from flask import *

from database import *

public = Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template("home.html")

@public.route('/login',methods=['get','post'])
def login():
    if 'submit' in request.form:
        username = request.form['uname']
        password = request.form['pswd']

        print(username,"()")
        print(password,"()")
        qry="select * from login where username='%s' and password='%s'" %(username,password)
        a=select(qry)
        if a:
            session['log']=a[0]['login_id']
            if a[0]['usertype']=='admin':
                return redirect(url_for('admin.admin_home'))
            elif a[0]['usertype']=='farmer':
                q="select * from farmer where login_id='%s'"%(session['log'])
                r=select(q)
                if r:
                    session['fam']=r[0]['farmer_id']
                return redirect(url_for('farmer.farmer_home'))

    return render_template("login.html")


@public.route('/registration',methods=['get','post'])
def registration():
    if 'register' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        place = request.form['place']
        phoneno = request.form['phoneno']
        emailid = request.form['emailid']
        username = request.form['username']
        password = request.form['password']

        print(firstname,lastname,place,phoneno,emailid,username,password)

        z="insert into login values(null,'%s','%s','farmer')"%(username,password)
        id=insert(z)

        x="insert into farmer values(null,'%s','%s','%s','%s','%s','%s')"%(id,firstname,lastname,place,phoneno,emailid)
        insert(x)

        return redirect(url_for('public.login'))

    return render_template("registration.html")



