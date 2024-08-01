from models import EvaluationRecords,Derived_records,Users
from flask_restful import Api, Resource
from flask import Flask,request,jsonify,make_response,g
from external import db
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import users_schema

class EvaluationRecord(Resource):      #接口名字可以随便起，但是后面那个路由要与这个对应起来
    def get(self):     #get请求
        records = EvaluationRecords.query.all()
        return records
    def post(self):    #post请求

        #获取前端输入的json数据，我们的数据同一默认都是json数据，方便使用，统一标准
        account=request.json['account']
        patient=Patient.query.filter(Patient.account==account).first()
        name=request.json['name']
        email=request.json['email']
        idnumber=request.json['idnumber']
        try:             #数据库的事务，保证数据的一致性，进行一下异常捕获，具体可以去看flask中的数据库使用细节
            patient.name=name         #数据库操作
            patient.email=email
            patient.idnumber=idnumber
            db.session.commit()
        except:
            db.session.rollback()
        return {"mag":"modify is success"}        #返回提示信息，均为json格式

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'phone_number')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class User(Resource):
    def get(self):
        users = Users.query.all()
        return users_schema.dump(users)
    def post(self):
        print(request.data)
        name = request.json['name']
        password = request.json['password']
        phone = request.json['phone']
        new_user = Users(username=name, password=password, phone_number=phone)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "User creation failed"}
        return {"message": "User created successfully"}




    