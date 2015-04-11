from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class Token(db.Model):
    env = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(80))
    datetime = db.Column(db.DateTime)

    def __init__(self, env, value, datetime):
        self.env = env
        self.value = value
        sele.datetime = datetime

    def __repr__(self):
        return '<env %r>' % self.env