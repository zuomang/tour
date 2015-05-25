#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/tour'
db = SQLAlchemy(app)

member = db.Table('member',
    db.Column('custormer_id', db.String(40), db.ForeignKey('custormer.openid')),
    db.Column('qun_id', db.Integer, db.ForeignKey('qun.id')),
)


class Custormer(db.Model):
    openid = db.Column(db.String(40), primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    phone = db.Column(db.String(11), unique=True, nullable = False)
    register_time = db.Column(db.DateTime, default = datetime.now())
    rank = db.Column(db.Integer, default = 1)
    quns = db.relationship('Qun', secondary=member,
            backref = db.backref('custormers', lazy = 'dynamic'))

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
    building_fund = db.Column(db.Float, default = 0)
    extracted_fund = db.Column(db.Float, default = 0)
    balance_fund = db.Column(db.Float, default = 0)
    openid = db.Column(db.String(40), db.ForeignKey('custormer.openid'))

    def __init__(self, name, phone, openid):
        self.name = name
        self.phone = phone
        self.openid = openid

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
    partici_fee = db.Column(db.Float, nullable = False)
    cost = db.Column(db.Float, nullable = False)
    is_join = db.Column(db.String(1), nullable = False, default = 'Y')
    datetime = db.Column(db.String(20), nullable = False)
    activity_details = db.relationship('ActivityDetail', backref = 'activity', lazy = 'dynamic')

    def __init__(self, name, owner, partici_fee, cost):
        self.name = name
        self.owner = owner
        self.partici_fee = partici_fee
        self.cost = cost

    def __repr__(self):
        return '<Activity %r>' % self.name


class ActivityDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    activity_name = db.Column(db.String(20), nullable = False)
    activity_date = db.Column(db.String(20), nullable = True)
    qunownr_id = db.Column(db.String(28), nullable = False)
    custormer_id = db.Column(db.String(28), nullable = False)
    accompany_count = db.Column(db.Integer, nullable = False)
    activity_pay = db.Column(db.Float, nullable = False)
    qunbuilding_return = db.Column(db.Float, nullable = False)

    def __init__(self, activity_id, activity_name, qunownr_id,
            custormer_id, accompany_count, activity_pay, qunbuilding_return):
        self.activity_id = activity_id
        self.activity_name = activity_name
        # self.activity_date = activity_date
        self.qunownr_id = qunownr_id
        self.custormer_id = custormer_id
        self.accompany_count = accompany_count
        self.activity_pay = activity_pay
        self.qunbuilding_return = qunbuilding_return

    def __repr__(self):
        return '<ActivityDetail %r>' % self.id


class PaymentOrder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bank_type = db.Column(db.String(16))
    cash_fee = db.Column(db.String(32))
    fee_type = db.Column(db.String(8))
    is_subscribe = db.Column(db.String(1))
    openid = db.Column(db.String(32))
    out_trade_no = db.Column(db.String(32))
    result_code = db.Column(db.String(16))
    time_end = db.Column(db.String(14))
    total_fee = db.Column(db.String(20))
    trade_type = db.Column(db.String(16))
    transaction_id = db.Column(db.String(32))

    def __init__(self, bank_type, cash_fee, fee_type, is_subscribe, openid, out_trade_no,
            result_code, time_end, total_fee, trade_type, transaction_id):
        self.bank_type = bank_type
        self.cash_fee = cash_fee
        self.fee_type = fee_type
        self.is_subscribe = is_subscribe
        self.openid = openid
        self.out_trade_no = out_trade_no
        self.result_code = result_code
        self.time_end = time_end
        self.total_fee = total_fee
        self.trade_type = trade_type
        self.transaction_id = transaction_id

    def __repr__(self):
        return '<PaymentOrder %r>' % self.id

if __name__ == "__main__":
	db.drop_all()
	db.create_all()
