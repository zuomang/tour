#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)

member = db.Table('member',
	db.Column('custormer_id', db.String(40), db.ForeignKey('custormer.openid')),
	db.Column('qun_id', db.Integer, db.ForeignKey('qun.id')),
)

class Custormer(db.Model):
	__bind_key__ = 'custormer'
	Openid = db.Column(db.String(40), primary_key=True)
	Username = db.Column(db.String(20), unique=True, nullable = False)
	Phone = db.Column(db.String(11), unique=True, nullable = False)
	Register_Time = db.Column(db.DateTime, default = datetime.now())
	Rank = db.Column(db.Integer, default = 1)
	Quns = db.relationship('Qun', secondary=member,
		backref = db.backref('Custormers', lazy = 'dynamic'))

	def __init__(self, openid, username, phone):
		self.openid = openid
		self.username = username
		self.phone = phone

	def __repr__(self):
		return '<User %r>' % self.username

class Qun(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable = False)
	name = db.Column(db.String(20), unique=True, nullable = False)
	phone = db.Column(db.String(11))
	register_time = db.Column(db.DateTime, default = datetime.now())
	rank = db.Column(db.Integer, nullable = False, default = 1)
	member_count = db.Column(db.Integer, default = 1)
	building_fund = db.Column(db.Integer, default = 0)
	extracted_fund = db.Column(db.Integer, default = 0)
	balance_fund = db.Column(db.Integer, default = 0)
	openid = db.Column(db.String(40), db.ForeignKey('custormer.openid'))

	def __init__(self, name, phone, openid, building_fund):
		self.name = name
		self.phone = phone
		self.openid = openid
		self.building_fund = building_fund

	def __repr__(self):
		return '<Qun %r>' % self.name

class Token(db.Model):
	name = db.Column(db.String(20), primary_key=True)
	token = db.Column(db.String(150), nullable=False)
	time = db.Column(db.DateTime, default=datetime.now())

	def __init__(self, name, token):
		self.name = name
		self.token = token

	def __repr__(self):
		return '<Token %r>' % self.name

class Activity(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20), nullable = False)
	owner = db.Column(db.String(28), nullable = False)
	description = db.Column(db.String(200))
	partici_fee = db.Column(db.String(20), nullable = False)
	cost = db.Column(db.String(20), nullable = False)

	def __init__(self, name, owner, partici_fee, cost):
		self.name = name
		self.owner = owner
		self.partici_fee = partici_fee
		self.cost = cost

	def __repr__(self):
		return '<Activity %r>' % self.name

class ActivityDetail(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	Activity_Id = db.Column(db.Integer, db.ForeignKey('Activity.id'))
	Activity_Name = db.Column(db.String(20), nullable = False)
	Activity_Date = db.Column(db.String(20), nullable = False)
	Qun_Id = db.Column(db.Integer, db.ForeignKey('Qun.id'))
	Custormer_Id = db.Column(db.String(20), db.ForeignKey('Custormer.openid'))
	Accompany_Count = db.Column(db.Integer, nullable = False)
	Activities_Pay = db.Column(db.Integer, nullable = False)
	QunBuilding_Return = db.Column(db.Integer, nullable = False)

	def __init__(self, Activity_Id, Activity_Name, Activity_Date, Qun_Id, Custormer_Id, Accompany_Count, Activities_Pay, QunBuilding_Return):
		self.Activity_Id = Activity_Id
		self.Activity_Name = Activity_Name
		self.Activity_Date = Activity_Date
		self.Qun_Id = Qun_Id
		self.Custormer_Id = Custormer_Id
		self.Accompany_Count = Accompany_Count
		self.Activities_Pay = Activities_Pay
		self.QunBuilding_Return = QunBuilding_Return

	def __repr(self):
		return '<ActivityDetail %r>' % self.ActivityDetail


if __name__ == '__main__':
	db.create_all()
