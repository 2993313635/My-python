import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from flask import Flask, g
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.orm import sessionmaker

#flask相关变量声明
app = Flask(__name__)
api = Api(app)

#认证
auth = HTTPTokenAuth(scheme='Token')
tokens = {"siekdnwei",
          "viwneigjwejw"}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        g.current_user = token
        return token
    return False


#数据库相关操作

engine = sqlalchemy.create_engine("mysql+pymysql://root:boshuo@localhost:3306/restful_api",echo=False)
base = sqlalchemy.orm.declarative_base()

#构建数据模型User
class User(base):
    __tablename__ = 'Users'

    #构建表结构
    id = sqlalchemy.Column("id",sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column("name",sqlalchemy.String(50), nullable=False)
    age = sqlalchemy.Column("age",sqlalchemy.Integer, nullable=False)


#构建数据模型的json格式
def get_json(user):
    return {"id":user.id,"name":user.name,"gae":user.age}

#使用session连接数据库
DBsession = sqlalchemy.orm.scoped_session(sessionmaker(bind=engine))
session = DBsession()
base. metadata.drop_all(engine)
base. metadata.create_all(engine)

#设置RESTfulAPI的参数解析规则   put,post参数
parser_put = reqparse.RequestParser()  #通过调用reqparse.RequestParser() 创建一个解析器对象用于解析参数
parser_put.add_argument('name',type=str,required=True,help="incoming data error,location='json")
parser_put.add_argument('age',type=int,required=True,help="incoming data error,location='json")

#设置get参数解析规则
parser_get = reqparse.RequestParser()
parser_get.add_argument("limit",type=int,required=False)
parser_get.add_argument("offset",type=int,required=False)
parser_get.add_argument("sortby",type=str,required=False)

#操作单一用户资源
class Todo(Resource):
    #添加认证
    decorators = [auth.login_required]  #定义了一个列表变量，其中有个装饰器，用于要求用户在访问方法时必须先进行登录验证

    def put(self,user_id):
        args = parser_put.parse_args()
        user_ids_set = set([user.id for user in session.query(User.id)])
        print(user_ids_set)

        #如果用户不存在，返回404
        if user_id not in user_ids_set:
            return None,404

        #更新用户数据
        user = session.query(User).filter(User.id == user_id)[0]
        user.name = args["name"]
        user.age = args["age"]
        session.merge(user)  #将更新的对象合并到会话中
        session.commit()

        #更新成功，返回201

        return get_json(user),201


#获取用户数据
    def get(self,user_id):
        users = session.query(User).filter(User.id == user_id)

        #用户不存在，返回404
        if users.count() == 0:
            return None,404

        #用户存在返回用户数据
        return get_json(users[0]),200

#删除用户数据
    def delete(self,user_id):
        session.query(User).filter(User.id == user_id).delete()
        return None,204

#操作post，grt资源列表
class TodoList(Resource):
    #添加认证
    decorators = [auth.login_required]
#获取全部用户数据
    def get(self):
        args = parser_get.parse_args()
        users = session.query(User)

        #根据条件查询
        if "srtby" in args:
            users = users.order_by(User.name if args["srtby"] =="name" else User.age)
        if "limit" in args:
            users = users.limit(args["limit"])
        if "offset" in args:
            users = users.offset(args["offset"])

        #返回结果
        return [get_json(user) for user in users],200

#添加一个新用户
    def post(self):
        args = parser_put.parse_args()

        #构建新用户
        user = User(name=args["name"],age=args["age"])
        session.add(user)
        session.commit()

        #添加成功，返回201
        return get_json(user),201

#设置路由
api.add_resource(Todo,"/users/<int:user_id>")
api.add_resource(TodoList,"/users/")

if __name__ == '__main__':
    app.run()



