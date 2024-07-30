from flask import Flask,request,jsonify,make_response,g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import external
from external import db
from models import EvaluationRecords,Derived_records
import requests,json
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
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



@app.route("/")  #将根URL映射到hello_world函数上
def hello_world():  #定义视图函数
    return "Hello World!"

if __name__ == '__main__':        #运行flask
    app.run(host="0.0.0.0",port=5000,debug=True)
