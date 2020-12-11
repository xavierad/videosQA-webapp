from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import datetime
from os import path

# SQL access layer initialization
DATABASE_FILE = "QandA.sqlite"
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
    #time = Column(String)
    #user = Column(String)

    def __repr__(self):
        return "<Question (id=%d Question=%s>" % (self.id, self.question)

    def to_dictionary(self):
        return {"question_id": self.id, "question": self.question}



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sql_session = scoped_session(Session)


def listQuestions():
    return sql_session.query(Question).all()
    sql_session.close()

def listQuestionsDICT():
    ret_list = []
    lq = listQuestions()
    print(lq)
    for q in lq:
        quest = q.to_dictionary()
        ret_list.append(quest)
    return ret_list

def getQuestion(id):
    q =  sql_session.query(Question).filter(Question.id==id).first()
    sql_session.close()
    return q

def getQuestionDICT(id):
    return getQuestion(id).to_dictionary()


def newQuestion(question):
    q = Question(question = question)
    try:
        sql_session.add(q)
        sql_session.commit()
        print(q.id)
        sql_session.close()
        return q.id
    except Exception as e:
        print(e)
        return None



if __name__ == "__main__":
     pass