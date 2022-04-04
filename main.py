from flask import Flask, request, url_for, render_template, session, redirect, abort, flash, g
from DataBase import DataBase
import pyautogui 
import sqlite3
import time
import os



DATABASE = 'datas.db'
DEBUG = True
SECRET_KEY = 'asdfasagsdg^76&*^&@^&as:dfasdfasdFSWfasd34534dfgSD5653__6547^&(%^&*&*(^#^#()#%@(FDSGDA?AS"DE|'

app = Flask(__name__)
app.config.from_object(__name__)

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




@app.route('/')
def index():
    db = get_db()
    dbase = DataBase(db)

    return render_template('index.html', posts=dbase.getMenu())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link,db'):
        g.link_db.close()


@app.route('/sing-in', methods=['POST', 'GET'])
def Log_in():
    db = get_db()
    dbase = DataBase(db)

    if request.method == 'POST': 
        session['userLogged'] = request.form['username']
        result = dbase.singAccount(request.form['username'], request.form['userpassword'])
        if result:
            return redirect(url_for('profile', username=session['userLogged'])) 
        
        else:
            return redirect(url_for('regisration'))

    return render_template('singin.html', menu=dbase.getMenu())




@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    dbase = DataBase(db)

    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    session.clear()
    return render_template('profile.html', name=f'{username}', title='profile')





@app.route('/regisration', methods=['POST', 'GET'])
def regisration():
    db = get_db()
    dbase = DataBase(db)
    dirname = 'users/'

    try:
        if request.method == 'POST':
            session['userLogged'] = request.form['usernamereg']
            if len(request.form['usernamereg']) > 1 and len(request.form['user-password']) >= 4:
                result = dbase.addAccount(request.form['usernamereg'], request.form['user-password'])
                if not result:
                    flash('Помилка реєстації акаунта', category='error')
                else:
                    dirname += request.form['usernamereg']
                    os.mkdir(dirname)
                    flash('Вхід був успішно виконаний', category='success')
                    

                    return redirect(url_for('profile', username=session['userLogged']))
                
            else:
                flash('Помилка реєстації. Ім*я має місити не менше 1 символа, а пароль 4', category='error')
        
    
    except FileExistsError:
        flash('Такий профіль вже існує!', category='error')

    return render_template('regisration.html')

if __name__ == "__main__":
    app.run(debug=True)
    