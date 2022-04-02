from flask import Flask, request, url_for, render_template, session, redirect, abort, flash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasagsdg^76&*^&@^&#%@(FDSGDA?AS"DE|'

db = sqlite3.connect('dates.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    password TEXT,
    date_created TEXT
)""")
db.commit()


# sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", ('test@gmail.com', 
# 'andrew177', '2342342', datetime.utcnow()))
# db.commit()


# sql.execute("DELETE FROM users WHERE email='';")
# db.commit()

# for i in sql.execute('SELECT email, name, password, date_created FROM users'):
#     print('emails-', i[0], 'names-', i[1], 
#                 'pass-', i[2],  'time-', i[3][:16])



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log-in', methods=['POST', 'GET'])
def Log_in():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    
    elif request.method == 'POST': 
        # якщо таке імя вже, то закинути на реєстацію
        session['userLogged'] = request.form['username']
        
        
        a, b = request.form['username'], request.form['userpassword']
        print(a, b)
        for i in sql.execute("SELECT `name` FROM users"):
            print(i)
       

        sql.execute(f'SELECT name, password FROM users WHERE name = "{a}" AND password = "{b}"')
        if sql.fetchone() is None:
            return redirect(url_for('regisration'))
        
        else:
            return redirect(url_for('profile', username=session['userLogged']))

    return render_template('log_in.html')

@app.route('/profile/<username>')
def profile(username):
    """_summary_

    Args:
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    session.clear()
    return f'Профіль користувача: {username} <br><a href="/">Exit</a>'


@app.route('/regisration')
def regisration():
    login, password = request.form['username'], request.form['userpassword']
    print(login, password)
    # sql.execute(f"SELECT login FROM users WHERE login = '{login}'")    
    # if sql.fetchone() is None:
    #     sql.execute(f"INSERT INTO users VALUES (?, ?)", (login, user-password))
    #     db.commit()
    #     print('Ви зареєстували свій акаунт!')
    
    # else:
    #     print('Такий акаунт вже існує!')

    return render_template('regisration.html')



if __name__ == "__main__":
    app.run(debug=True)
    