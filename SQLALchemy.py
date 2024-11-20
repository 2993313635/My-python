import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

engine = sqlalchemy.create_engine("mysql+pymysql://root:boshuo@localhost:3306 /测试",echo=False)

Base = sqlalchemy.ext.declarative.declarative_base()

class User(Base):
     __tablename__ = 'Users'
     __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
     name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
     age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

     role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Roles.id'))
     role = sqlalchemy.orm.relationship("Role", foreign_keys="User.role_id")


class Role(Base):
     __tablename__ = 'Roles'
     __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
     name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)

     users = sqlalchemy.orm.relationship("User", foreign_keys="User.role_id")

DBSessinon = sqlalchemy.orm.sessionmaker(bind=engine)   # 创建会话类
session = DBSessinon()

# 删除所有表
Base.metadata.drop_all(engine)
# 创建所有表,如果表已经存在,则不会创建
Base.metadata.create_all(engine)

#清空表
session.query(User).filter(User.id != -1).delete()
session.query(Role).filter(Role.id != -1).delete()


session.add(Role(id=1, name="studest"))
session.add(Role(id=2, name="teacher"))
session.commit()

session.add(User(name="张三", age=18, role_id=1))
session.add(User(name="李四", age=19, role_id=2))
session.commit()

user = User(name="Kobe", age=24, role_id=1)
session.add(user)
session.commit()


roles = session.query(Role)
for role in roles:
    print("Role:", role.id, role.name)

users = session.query(User)
for user in users:
    print("User:", user.id, user.name, user.age, user.role_id)

users = session.query(User).filter(User.id > 6)
users = session.query(User).filter(User.id > 6).all()
users = session.query(User).filter(User.id > 6).limit(10)
users = session.query(User).filter(User.id > 6).offset(2)
users = session.query(User).filter(User.id > 6, User.name == "Kobe")
users = session.query(User).filter(User.id > 6).filter(User.name == "Kobe")
users = session.query(User).filter(sqlalchemy.or_(User.id > 6, User.name == "Kobe"))
users = session.query(User).filter(User.id.in_((1, 2)))
users = session.query(User).filter(sqlalchemy.not_(User.name))

user_count = session.query(User.id).count()
user_count = session.query(sqlalchemy.func.count(User.id)).scalar()
session.query(sqlalchemy.func.count("*")).select_from(User).scalar()
session.query(sqlalchemy.func.count(1)).select_from(User).scalar()
session.query(sqlalchemy.func.count(User.id)).filter(User.id > 0).scalar()

session.query(sqlalchemy.func.sum(User.age)).scalar()
session.query(sqlalchemy.func.avg(User.age)).scalar()
session.query(sqlalchemy.func.md5(User.name)).filter(User.id == 1).scalar()

session.close()
