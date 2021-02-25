import sqlite3

from flask import Flask, g, redirect, render_template, request
import socket
DATABASE = 'database.db'

app = Flask(__name__, template_folder='templates')

host =socket.gethostname()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    with app.open_resource('data.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route("/", methods=['GET', 'POST'])
def easy():
    message = 'Lvl 1: very dễ không cần trick , username là \'admin\'.'
    error = ''
    if request.form:
        cur = get_db().cursor()
        cur.execute(f"SELECT name, password FROM users WHERE name='{request.form['username']}' and password='{request.form['password']}';")
        if len(cur.fetchall()) > 0:
            return redirect('/medium')
        else:
            error = 'Simple lóp , téo tèo teo'
    return render_template('easy.html', message=message, error=error)


@app.route("/medium", methods=['GET', 'POST'])
def medium():
    message = 'Lvl 2: Khó hơn 1 chút, 1 chút thôi!'
    error = ''
    if request.form:
        cur = get_db().cursor()
        username = request.form['username'].replace("--", "")
        #username = request.form['username'].replace("'", "")
        password = request.form['password'].replace("--", "")
        cur.execute(f"SELECT name, password FROM users WHERE name='{username}' and password='{password}';")
        if len(cur.fetchall()) > 0:
            return redirect('/hard')
        else:
            error = 'Simple lóp , téo tèo teo'
    return render_template('easy.html', message=message, error=error)


@app.route("/hard", methods=['GET', 'POST'])
def hard():
    message = 'Lvl 3: Amazing gút dóp ! Tới đây chỉ có m thôi phúc à :)))'
    error = ''
    if request.form:
        cur = get_db().cursor()
        username = request.form['username']
        password = request.form['password']
        username = username.replace(r"--", r"").replace(r"'", r"\'")
        password = password.replace(r"--", r"").replace(r"'", r"\'")
        query_str = f"SELECT name, password FROM users WHERE name='{username}' and password='{password}';"
        cur.execute(query_str)
        if len(cur.fetchall()) > 0:
            # solution: username='admin', password="'/*"
            message = 'Chúc mừng '+ socket.gethostbyname(host) + ' đã hoàn thành challenge!'
        else:
            error = 'Simple lóp , téo tèo teo'
    return render_template('easy.html', message=message, error=error)
if __name__=="__main__":
    app.run()