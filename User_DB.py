from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime
from os import path

# SQL access layer initialization
DATABASE_FILE = "Users.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class User(Base):
    __tablename__ = 'User'
    id = Column(String, primary_key=True)
    name = Column(String)
    videoRegistrations = Column(Integer, default = 0)
    # url = Column(String)
    # views = Column(Integer, default = 0)

    def __repr__(self):
        return "<User id=%s Name=%s videoRegistrations=%d>" % (self.id, self.name, self.videoRegistrations)

    def to_dictionary(self):
        return {"user_id": self.id, "name": self.name, "video_registrations": self.videoRegistrations}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
sql_session = scoped_session(Session)
# session = Session()

def newVideoRegist(user_id):
    b = sql_session.query(User).filter(User.id==user_id).first()
    b.videoRegistrations += 1
    n = b.videoRegistrations
    sql_session.commit()
    sql_session.close()
    return n

def listUsers():
    return sql_session.query(User).all()
    sql_session.close()

def listUsersDICT():
    ret_list = []
    lv = listUsers()
    print(lv)
    for v in lv:
        vd = v.to_dictionary()
        # del(vd["url"])
        # del(vd["views"])
        ret_list.append(vd)
    return ret_list

def getUser(id):
    v =  sql_session.query(User).filter(User.id==id).first()
    sql_session.close()
    return v

def getUserDICT(id):
    return getUser(id).to_dictionary()

def newUser(id, name):
    usr = User(id=id, name=name)
    print(usr.id)
    try:
        sql_session.add(usr)
        sql_session.commit()
        print(usr.id)
        sql_session.close()
        return usr.id
    except IntegrityError:
        return {}
    except: 
        return None