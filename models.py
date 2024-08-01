from external import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class EvaluationRecords(db.Model):
    __tablename__ = 'evaluation_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    car_series = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    derived_records = db.relationship('Derived_records', backref='evaluation_records', 
                            cascade='all, delete-orphan', passive_deletes=True)

class Derived_records(db.Model):
    __tablename__ = 'derived_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    evaluationid = db.Column(db.Integer, db.ForeignKey('evaluation_records.id'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# Below is the code of c:\Users\cwf\Desktop\Stellantis\external.py 
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    derived_records = db.relationship('Derived_records', backref='users', 
                            cascade='all, delete-orphan', passive_deletes=True)
    evaluation_records = db.relationship('EvaluationRecords', backref='users', 
                            cascade='all, delete-orphan', passive_deletes=True)
