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


@app.route('/log-in', methods=['POST', 'GET'])
def Log_in():
    db = get_db()
    dbase = DataBase(db)
    dirname = 'users/'

    if request.method == 'POST': 
        session['userLogged'] = request.form['username']
        if len(request.form['username']) > 1 and len(request.form['userpassword']) >= 4:
            result = dbase.addAccount(request.form['username'], request.form['userpassword'])
            if not result:
                flash('Помилка додавання статті', category='error')
            else:
                dirname += request.form['username']
                os.mkdir(dirname)
                flash('Вхід був успішно виконаний', category='success')
                

                return redirect(url_for('profile', username=session['userLogged']))
        
        else:
            flash('Помилка входу. Ім*я має місити не менше 1 символа, а пароль 4', category='error')
            
        
        

    return render_template('log_in.html', menu=dbase.getMenu())




@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    dbase = DataBase(db)

    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    session.clear()
    return render_template('profile.html', name=f'{username}')





@app.route('/regisration')
def regisration():
#     login, password = request.form['username'], request.form['userpassword']
#     print(login, password)
   
    return render_template('regisration.html')



if __name__ == "__main__":
    app.run(debug=True)
    