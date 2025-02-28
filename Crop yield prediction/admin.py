from flask import *

from database import *

admin = Blueprint('admin',__name__)

farmer = Blueprint('farmers',__name__)


@admin.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@admin.route('/view_farmers')
def view_farmers():
    qry = "SELECT * FROM farmer"
    farmers = select(qry)
    return render_template('view_farmers.html', farmers=farmers)

@admin.route('/view_fertilizer')
def view_fertilizer():
    qry = "SELECT * FROM fertilizer"
    fertilizer = select(qry)
    return render_template('view_fertilizer.html', fertilizer=fertilizer)


@admin.route('/add_fertilizer',methods=['get','post'])
def add_fertilizer():
    data={}

    qry="select * from fertilizer"
    res=select(qry)
    if res:
        data['view']=res
        
    if 'action' in request.args:
        act=request.args['action']
        fid=request.args['id']
    else:
        act=None
        
    if act == 'update':
        q="select * from fertilizer where fertilizer_id='%s'"%(fid)
        r=select(q)
        data['up']=r

    if 'update' in request.form:
        fertilizer = request.form['fertilizer']
        crop = request.form['crop']
        description = request.form['description']

        qry2="update fertilizer set fertilizer='%s',crop='%s',description='%s' where fertilizer_id='%s'"%(fertilizer,crop,description,fid)
        update(qry2)

        return "<script>alert('Updated');window.location='add_fertilizer'</script>"


    if act == 'delete':
        qry3 = "delete from fertilizer where fertilizer_id='%s'" % (fid)
        delete(qry3)

        return "<script>alert('successfully deleted');window.location='add_fertilizer'</script>"

    if 'add' in request.form:
        fertilizer = request.form['fertilizer']
        crop = request.form['crop']
        description = request.form['description']

        print(fertilizer,crop,description)

        y="insert into fertilizer values(null, '%s','%s','%s')"%(fertilizer,crop,description)
        insert(y)

        return "<script>alert('successfully added');window.location='add_fertilizer'</script>"
        
    return render_template("add_fertilizer.html",data=data)



@admin.route('/add_notification',methods=['get','post'])
def add_notification():
    data={}

    qry="select * from notification"
    res=select(qry)
    if res:
        data['view']=res

    if 'add' in request.form:
        notification = request.form['notification']
        date = request.form['date']

        print(notification,date)

        y="insert into notification values(null,'%s','%s')"%(notification,date)
        insert(y)

        return "<script>alert('successfully added');window.location='add_notification'</script>"


    return render_template("add_notification.html",data=data)


@admin.route('/reply_complaint',methods=['get','post'])
def reply_complaint():
    data={}

    qry="select * from complaint"
    res=select(qry)
    if res:
        data['view']=res

    if 'action' in request.args:
        act=request.args['action']
        cid=request.args['id']

        if act == 'reply':
            q="select * from complaint where complaint_id='%s'"%(cid)
            r=select(q)
            data['reply']=r

            if 'add' in request.form:
                reply = request.form['reply']

                print(reply)

                y="update complaint set reply='%s' where complaint_id='%s'"%(reply,cid)
                update(y)

                return "<script>alert('reply added');window.location='reply_complaint'</script>"

    return render_template("reply_complaint.html",data=data)


@admin.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user session
    return redirect(url_for('public.login'))  # Redirect to login page


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authenticate user here
        session['user_id'] = user.id  # Set user session after successful login
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    return render_template('login.html')


    