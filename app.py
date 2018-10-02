from flask import Flask, render_template, g, request, redirect, url_for
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
import os
# import sqlite3
from flask_sqlalchemy import SQLAlchemy

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(extensions=[HamlishExtension])

app = FlaskWithHamlish(__name__)

db_uri = 'sqlite:///' + os.path.join(app.root_path, 'flasknote.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)

@app.route('/')
def hello_world():
    # entries = get_db().execute('SELECT title, body FROM entries').fetchall()
    entries = Entry.query.all()
    return render_template('index.haml', entries=entries)

@app.route('/post', methods=['POST'])
def add_entry():
    entry = Entry()
    entry.title = request.form['title']
    entry.body = request.form['body']
    db.session.add(entry)
    db.session.commit()
    
    return redirect(url_for('hello_world'))

# def connect_db():
#     db_path = os.path.join(app.root_path, 'flasknote.db')
#     rv = sqlite3.connect(db_path)
#     rv.row_factory = sqlite3.Row
#     return rv

# def get_db():
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()