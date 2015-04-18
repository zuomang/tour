#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class Custormer(db.Model):
    openid = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    phone_number = db.Column(db.Integer, unique=True, nullable = False)
    qunowner1_phone = db.Column(db.Integer)
    qunowner2_phone = db.Column(db.Integer)
    qunowner3_phone = db.Column(db.Integer)
    qunowner4_phone = db.Column(db.Integer)
    qunowner5_phone = db.Column(db.Integer)
    qunowner6_phone = db.Column(db.Integer)
    qunowner7_phone = db.Column(db.Integer)
    qunowner8_phone = db.Column(db.Integer)

    def __init__(self, openid, username, phone):
        self.openid = openid
        self.username = username
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    db.create_all()