from flask import (Flask, render_template, url_for, request, session,
                    flash, redirect, g, abort, make_response)

from flask_login import (LoginManager, login_user, login_required, 
                            logout_user, current_user)

from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from UserLogin import UserLogin
from DataBase import DataBase
import datetime
import sqlite3



# config
DATABASE = 'datas.db'
DEBUG = True
SECRET_KEY = 'asdfasag^&asdfasdfasd3453dfgSD565asdSWf3__*(()#%@(FDSGDA?AS"DE|'
MAX_CONTENT_LENGTH = 1024 * 1024 * 10


app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйся, щоб читати вміст сайту'
login_manager.login_message_category = 'error'




@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    
    return connection

def create_db():
    db = connect_db()
    with app.open_resource('commands.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    
    return g.link_db

def count_update():
    db = get_db()
    dbase = DataBase(db)
    if datetime.datetime.now().hour == 0:
        dbase.countsUpdate()


temp = ''
dbase = None
@app.before_request
def before_request():
    """connection with db afther request"""
    global dbase
    db = get_db()
    dbase = DataBase(db)


@app.route('/')
def index():
    count_update()

    return render_template('index.html', posts=dbase.showallaccounts())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link,db'):
        g.link_db.close()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
        
        flash('incorrect login/password', category='error')

    return render_template('login.html', title='Авторизація', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashpass = generate_password_hash(form.password.data)
        result = dbase.addUser(form.name.data, form.email.data, hashpass)
        if result:
            flash('Ви успішно зареєструвалися', 'success')
            return redirect(url_for('profile'))

        else:
            flash('Помилка при додаванні даних в БД', category='error')

    return render_template('register.html', title='Реєстрація', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви покинули профіль', category='success')

    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    count_update()

    return render_template('profile.html', tile='Профіль')


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ''

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                result = dbase.updateUserAvatar(img, current_user.get_id())
                if not result:
                    flash('Помилка оновлення аватару', category='error')
                   
                flash('Аватарка оновлена', category='success')
            except FileNotFoundError as e:
                flash('Помилка читання файлу', category='error')
        else:
            flash('Помилка оновлення аватки', category='error')

    return redirect(url_for('profile'))



@app.route('/profile/game')
def game():
    if not dbase.play(current_user.getName()):
        flash('Ви вичерпали всі спроби на сьогодні', category='error')

    return render_template('game.html')



if __name__ == "__main__":
    app.run(debug=True)
    