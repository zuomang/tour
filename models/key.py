from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class Key(db.Model):
    token = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(80))
    time = db.Column(db.DateTime)

    def __init__(self, token, value, time):
        self.token = token
        self.value = value
        self.time = time

    def __repr__(self):
        return '<token %r>' % self.token

if __name__ == '__main__':
    db.create_all()