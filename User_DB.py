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

# Declaration of data regarding a user
class User(Base):
    __tablename__ = 'User'
    id = Column(String, primary_key=True) # the user id is defined as the primary key
    name = Column(String) # the user name
    videoRegistrations = Column(Integer, default = 0) # the number os videos added by the user
    nviews = Column(Integer, default = 0) # the number of video views
    nquestions = Column(Integer, default = 0) # the number of questions made by the user
    nanswers = Column(Integer, default = 0) # the number of answers made by the user

    def __repr__(self):
        return "<User id=%s Name=%s videoRegistrations=%d number of views=%d number of questions=%d number of answers=%d>" % (self.id, self.name, self.videoRegistrations, self.nviews, self.nquestions, self.nanswers)

    def to_dictionary(self):
        return {"user_id": self.id, "name": self.name, "video_registrations": self.videoRegistrations, "nviews":self.nviews, "nquestions":self.nquestions, "nanswers":self.nanswers}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
sql_session = scoped_session(Session)
# session = Session()

# to query all users
def listUsers():
    return sql_session.query(User).all()
    sql_session.close()

# to get the list of dictionary users
def listUsersDICT():
    ret_list = []
    lv = listUsers()
    print(lv)
    for v in lv:
        vd = v.to_dictionary()
        ret_list.append(vd)
    return ret_list

# to query an user with an id
def getUser(id):
    v =  sql_session.query(User).filter(User.id==id).first()
    sql_session.close()
    return v

# to return a dictionary user
def getUserDICT(id):
    return getUser(id).to_dictionary()

# to increment number of video registered by an user
def newVideoRegist(user_id):
    b = sql_session.query(User).filter(User.id==user_id).first()
    b.videoRegistrations += 1
    n = b.videoRegistrations
    sql_session.commit()
    sql_session.close()
    return n

# to increment the number of visualized videos
def incrementViews(user_id):
    b = sql_session.query(User).filter(User.id==user_id).first()
    b.nviews += 1
    n = b.nviews
    sql_session.commit()
    sql_session.close()
    return n

# to increment the number of questions made
def incrementQuestions(user_id):
    b = sql_session.query(User).filter(User.id==user_id).first()
    b.nquestions += 1
    n = b.nquestions
    sql_session.commit()
    sql_session.close()
    return n

# to increment the number of answers made
def incrementAnswers(user_id):
    b = sql_session.query(User).filter(User.id==user_id).first()
    b.nanswers += 1
    n = b.nanswers
    sql_session.commit()
    sql_session.close()
    return n

# to add a new user
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
        