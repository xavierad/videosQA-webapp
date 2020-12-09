from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import datetime
from os import path

# SQL access layer initialization
DATABASE_FILE = "Q&A.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Question(Base):
    __tablename__ = 'Question'
    id = Column(Integer, primary_key=True)
    question = Column(String)

    def __repr__(self):
        return "<Question (id=%d Question=%s>" % (self.id, self.question)

    def to_dictionary(self):
        return {"question_id": self.id, "question": self.answer}

class Answer(Question):
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True)
    answer = Column(String)

    def __repr__(self):
        return "<Answer (id=%d Answer=%s>" % (self.id, self.answer)

    def to_dictionary(self):
        return {"answer_id": self.id, "answer": self.answer}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
sql_session = scoped_session(Session)
# session = Session()


def listQuestions():
    return sql_session.query(Question).all()
    sql_session.close()

def listQuestionsDICT():
    ret_list = []
    lq = listQuestions()
    print(lq)
    for q in lq:
        qa = q.to_dictionary()
        del(qa["url"])
        del(qa["views"])
        ret_list.append(qa)
    return ret_list

def getQuestion(id):
    q =  sql_session.query(Question).filter(Question.id==id).first()
    sql_session.close()
    return q

def getVideoDICT(id):
    return getVideo(id).to_dictionary()

def newVideoView(id):
    b = sql_session.query(Video).filter(Video.id==id).first()
    b.views+=1
    n = b.views
    sql_session.commit()
    sql_session.close()
    return n


def newVideo(description , url):
    vid = Video(description = description, url = url)
    try:
        sql_session.add(vid)
        sql_session.commit()
        print(vid.id)
        sql_session.close()
        return vid.id
    except:
        return None



# if __name__ == "__main__":
#     pass