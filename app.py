from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visits INTEGER DEFAULT 0,
            submissions INTEGER DEFAULT 0
        )
        """)
        cursor.execute("INSERT INTO stats (visits, submissions) VALUES (0, 0)")
        db.commit()

@app.before_request
def before_request():
    db = get_db()
    db.execute("UPDATE stats SET visits = visits + 1 WHERE id = 1")
    db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db = get_db()
        db.execute("UPDATE stats SET submissions = submissions + 1 WHERE id = 1")
        db.commit()
        return redirect(url_for('warning'))
    return render_template('index.html')

@app.route('/warning')
def warning():
    return render_template('warning.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
