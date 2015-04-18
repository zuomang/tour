#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class Custormer(db.Model):
    openid = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    phone_number = db.Column(db.Integer, unique=True, nullable = False)
	time = db.Column(db.DateTime)

    def __init__(self, openid, username, phone, register_time):
        self.openid = openid
        self.username = username
        self.phone_number = phone
		self.time = register_time

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    db.create_all()
