#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
db = SQLAlchemy(app)

tags = db.Table('tags',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

class Student(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20))

	courses = db.relationship('Course', secondary = tags, 
		backref = db.backref('students', lazy = 'dynamic'))
<<<<<<< HEAD

	def __init__(self, id, name):
		self.id = id
		self.name = name

class Course(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	teacher = db.Column(db.String(20))

	def __init__(self, id, teacher):
		self.id = id
		self.teacher = teacher

if __name__ == '__mian__':
	db.create_all()
=======

	def __init__(self, id, name):
		self.id = id
		self.name = name

class Course(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	teacher = db.Column(db.String(20))

	def __init__(self, id, teacher):
		self.id = id
		self.teacher = teacher

if __name__ == '__main__':
    db.create_all()
>>>>>>> affed5a72338980c5810b9051dcdfc6bc45ac102
