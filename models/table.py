#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)

class Custormer(db.Model):
    openid = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    phone_number = db.Column(db.String(11), unique=True, nullable = False)
    register_time = db.Column(db.DateTime, default = datetime.now())
    rank = db.Column(db.Integer, default = 1)
    qun = db.relationship('Qun', backref='custormer', lazy='dynamic')

    def __init__(self, openid, username, phone):
        self.openid = openid
        self.username = username
        self.phone_number = phone

    def __repr__(self):
        return '<User %r>' % self.username

class Qun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custormer_id = db.Column(db.String(40), db.ForeignKey('custormer.openid'))
    name = db.Column(db.String(20), unique=True, nullable = False)
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
        return '<qun %r>' % self.name

member = db.Table('member',
    db.Column('custormer_id', db.String(40), db.ForeignKey('custormer.openid')),
    db.Column('qun_id', db.Integer, db.ForeignKey('qun.id')),
    db.Column('qun_name', db.String(20), db.ForeignKey('qun.name'))

if __name__ == '__main__':
	db.create_all()
