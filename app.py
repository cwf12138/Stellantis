from flask import Flask,request,jsonify,make_response,g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import external
from external import db
from models import EvaluationRecords,Derived_records,Users
import requests,json
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 
# import jwt
import datetime
# import redis
app = Flask(__name__)
app.config.from_object(external)
api = Api(app, default_mediatype="application/json")
app.config['SECRET_KEY'] = 'thisissecret'
ma = Marshmallow(app)
db.init_app(app)

CORS(app, resources=r'/*')
# r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)     #redis 连接
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'phone_number')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class EvualtionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'brand', 'car_series', 'vehicle_type', 'created_at', 'updated_at')   
evualtion_schema = EvualtionSchema(many=True)



@app.route("/")  #将根URL映射到hello_world函数上
def hello_world():  #定义视图函数
    return "Hello World!"

class EvaluationRecord(Resource):      #接口名字可以随便起，但是后面那个路由要与这个对应起来
    def get(self):     #get请求
        records = EvaluationRecords.query.all()
        return evualtion_schema.dump(records)
    def post(self):    #post请求
        userid=request.json['userid']
        brand=request.json['brand']
        #获取前端输入的json数据，我们的数据同一默认都是json数据，方便使用，统一标准
        car_series=request.json['car_series']
        vehicle_type=request.json['vehicle_type']
        created_at=datetime.datetime.now()
        updated_at=datetime.datetime.now()
        new_record = EvaluationRecords(userid=userid, brand=brand, car_series=car_series, vehicle_type=vehicle_type, created_at=created_at, updated_at=updated_at)
        try:             #数据库的事务，保证数据的一致性，进行一下异常捕获，具体可以去看flask中的数据库使用细节
            db.session.add(new_record)
            db.session.commit()
        except:
            db.session.rollback()
        return {"mag":"modify is success"}        #返回提示信息，均为json格式
    def put(self):
        userid=request.json['userid']
        brand=request.json['brand']
        id = request.json['id']
        #获取前端输入的json数据，我们的数据同一默认都是json数据，方便使用，统一标准
        car_series=request.json['car_series']
        vehicle_type=request.json['vehicle_type']
        updated_at=datetime.datetime.now()
        record = EvaluationRecords.query.filter_by(id=id,userid=userid).first()
        try:
            record.brand = brand
            record.car_series = car_series
            record.vehicle_type = vehicle_type
            record.updated_at = updated_at
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

api.add_resource(User, '/user/')
api.add_resource(EvaluationRecord, '/record/')

if __name__ == '__main__':        #运行flask
    app.run(host="0.0.0.0",port=5000,debug=True)
