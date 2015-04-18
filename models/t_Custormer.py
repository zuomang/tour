#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class T_Custormer(db.Model):
    Openid = db.Column(db.String(80), primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable = False)
    Phone_Number = db.Column(db.Integer, unique=True, nullable = False)
    QunOwner1_Phone = db.Column(db.Integer)
    QunOwner2_Phone = db.Column(db.Integer)
    QunOwner3_Phone = db.Column(db.Integer)
    QunOwner4_Phone = db.Column(db.Integer)
    QunOwner5_Phone = db.Column(db.Integer)
    QunOwner6_Phone = db.Column(db.Integer)
    QunOwner7_Phone = db.Column(db.Integer)
    QunOwner8_Phone = db.Column(db.Integer)

    def __init__(self, openid, username, phone):
        self.openid = openid
        self.username = username
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    db.create_all()