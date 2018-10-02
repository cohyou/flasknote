from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
import os
import sqlite3

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(extensions=[HamlishExtension])

app = FlaskWithHamlish(__name__)

@app.route('/')
def hello_world():
    entries = get_db().execute('SELECT title, body FROM entries').fetchall()
    return render_template('index.haml', entries=entries)

def connect_db():
    db_path = os.path.join(app.root_path, 'flasknote.db')
    rv = sqlite3.connect(db_path)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()