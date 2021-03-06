#This program was created by qzo, as a self hosted replacement to neocities, so you can host your friend's simple webpages.
#This is a hobby project. Security is attempted, but not ensured. Do your best!


from flask import Flask, request, redirect, render_template, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from functools import wraps

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

from config import *
from util import *
db.create_all()
db.session.commit()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_logged_in():
            print "login failure"
            return redirect(url_for('login_handeler'))
        return f(*args, **kwargs)
    
    return decorated

@app.route('/')
def index_handeler():
    title="home"
    username = check_logged_in()
    return render_template("index.html", title=title, username=username)

@app.route('/register', methods = ['GET', 'POST'])
def register_handeler():
    username = check_logged_in()
 
    if request.method == 'POST':
        session.pop('username', None)
        if not request.form['username'] or not request.form['password'] or not request.form['password_check'] or not request.form['email']:
            flash('please check fields for completeness')
        else:
            username = request.form['username']
            email = request.form['email']
            password1 = request.form['password']
            password2 = request.form['password_check']
            if ( password1 == password2):
                create_status = usercreate(username, email, password1)
                if create_status == 1:
                    flash("User " + username + " created. Please log in.")
                if create_status == 2:
                    flash("User create failed, bad/taken username")
                if create_status == 3:
                    flash("User create failed, bad password")
                if create_status == 4:
                    flash("User create failed, a user already exists with this email")
                                    
            else:
                flash('passwords must match')
    return render_template('register_form.html', username=username)

@app.route('/login', methods = ['GET','POST'])
def login_handeler():
    username = check_logged_in()

    if request.method == 'POST':
        session.pop('username', None)
        
        if not request.form['username'] or not request.form['password']:
            flash('Please submit both your username and your password')
        else:
            username = request.form['username']
            password = request.form['password']
            loggedin = login(username, password)
            if loggedin == 1:
                flash("Successfully logged in")
            else:
                flash("Bad username or password")
    return render_template("login_form.html", username=username)
    

@app.route('/logout', methods = ['GET','POST'])
def logout_handeler():
    session.pop('username', None)
    flash('You are now successfully logged out')
    return render_template('logout.html')


@app.route('/dashboard', methods = ['GET'])
@requires_auth
def dashboard_handeler():
    '''if check_logged_in():
        username = check_logged_in()
        return render_template("dashboard.html", username=username)
    else:
        return redirect(url_for('login_handeler'))'''
    username = check_logged_in()
    return render_template("dashboard.html", username=username)

@app.route('/dashboard/new_site', methods = ['GET', 'POST'])
@requires_auth
def new_site_handeler():
    if request.method == 'POST':
        uploaded_files = request.files['file']
        print uploaded_files
        if 'file' not in request.files:
            flash('no file part')
            return redirect(request.url)
        elif not request.form['sitename'] and check_sitename(request.form['sitename']):
            flash('unique title required')
            return redirect(request.url)
        
        file = request.files['file']
        sitename = request.form['sitename']
        if file.filename == '':
            flash('no selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join('static/usersites/',secure_filename(file.filename)))
            create_site(file, sitename)
            flash("site uploaded")
            return redirect(request.url)
    username = check_logged_in()
    return render_template('new_site.html', username=username)














    ''''if request.method == "POST":

        if not request.form['title']:
            flash("Please title your site")
            return render_template('new_site.html', username=check_logged_in())
        else:
            
            username = check_logged_in()
            title = request.form['title']
            if 'sitefile' not in request.files:
                return redirect(url_for('dashboard_handeler'))
            file = request.files['sitefile']
            if file.filename == "":
                print file.filename
                print sitename                    
                flash('malformed file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/usersites/', filename))
                flash('site created, ', title)
               
                return redirect(url_for('dashboard_handeler'))
                
                        
        
    else:
        if check_logged_in():
            username = check_logged_in()
            print username
            return render_template('new_site.html', username = username)
        else:
            return redirect(url_for('login_handeler'))

        '''
if __name__ == '__main__':
        print(' * Database is', SQLALCHEMY_DATABASE_URI)
        print(' * Running on http://localhost:5000/ (Press Ctrl-C to quit)')
        app.run(host='0.0.0.0')

