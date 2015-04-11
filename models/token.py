#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class Token(db.Model):
    token = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    def __init__(self, token, value, date):
        self.token = token
        self.value = value
        self.date = date

    def __repr__(self):
        return '<Token %r>' % self.token