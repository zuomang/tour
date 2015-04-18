#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)


class Qun(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    custormer_id = db.Column(db.String(40), db.ForeignKey('custormer.openid'))
    name = db.Column(db.String(20), nullable = False)
    phone_number = db.Column(db.Integer, unique=True, nullable = False)
    register_time = db.Column(db.DateTime, default = datetime.now())
    rank = db.Column(db.Integer, nullable = False, default = 1)
    member_count = db.Column(db.Integer, default = 0)
    building_fund = db.Column(db.Integer, default = 0)
    extracted_fund = db.Column(db.Integer, default = 0)
    balance_fund = db.Column(db.Integer, default = 0)

    def __init__(self, custormer_id, name, phone_number):
        self.custormer_id = custormer_id
        self.name = name
        self.phone_number

    def __repr__(self):
        return '<User %r>' % self.name

if __name__ == '__main__':
    db.create_all()
