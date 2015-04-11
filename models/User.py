from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwaszx12@localhost/test'
db = SQLAlchemy(app)


class User(db.Model):
    openid = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(11), unique=True)

    def __init__(self, openid, username, phone):
        self.openid = openid
        self.username = username
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.username
