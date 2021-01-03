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

# Declaration of data regarding a question
class Question(Base):
    __tablename__ = 'Question'
    id = Column(Integer, primary_key=True) # question id is defined as the primary key
    question = Column(String) # the question text
    time = Column(String) # the time of the video when the question was made
    user = Column(String) # the user that made the question
    video_id = Column(Integer) # the video id that the question made corresponds to

    def __repr__(self):
        return "<Question (id=%d Question=%s User=%s Time=%s VideoID=%d)>" % (self.id, self.question, self.user, self.time, self.video_id)

    def to_dictionary(self):
        return {"question_id": self.id, "question": self.question, "user": self.user, "time": self.time, "video_id": self.video_id}

# Declaration of data regarding an answer
class Answer(Base):
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True) # the answer id is defined as the primary key
    answer = Column(String) # the answer text
    user_id = Column(String) # the user id that made the answer
    user_name = Column(String) # the user name of the user id
    question_id = Column(Integer) # the question id that the answer made corresponds to

    def __repr__(self):
        return "<Answer (id=%d Question_id=%d Answer=%s User_id=%s User_Name=%s)>" % (self.id, self.question_id, self.answer, self.user_id, self.user_name)

    def to_dictionary(self):
        return {"answer_id":self.id, "question_id":self.question_id, "answer":self.answer, "user_id":self.user_id, "user_name":self.user_name}


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sql_session = scoped_session(Session)

# Regarding Questions
# to query all questions (if any) corresponding to a video
def listQuestions(video_id):
    return sql_session.query(Question).filter(Question.video_id==video_id).all()
    sql_session.close()

# to get a list of dictionary questions of a video
def listQuestionsDICT(video_id):
    ret_list = []
    lq = listQuestions(video_id)
    print(lq)
    for q in lq:
        quest = q.to_dictionary()
        ret_list.append(quest)
    return ret_list

# to get single question
def getQuestion(id):
    q =  sql_session.query(Question).filter(Question.id==id).first()
    sql_session.close()
    return q

# to return a question dictionary
def getQuestionDICT(id):
    return getQuestion(id).to_dictionary()

# to add a new question
def newQuestion(question, user, time, video_id):
    q = Question(question=question, user=user, time=time, video_id=video_id)
    try:
        sql_session.add(q)
        sql_session.commit()
        print(q.id)
        sql_session.close()
        return q.id
    except Exception as e:
        print(e)
        return None

# Regarding Answers
# to get a list of answers (if any) for a question
def listAnswers(question_id):
    return sql_session.query(Answer).filter(Answer.question_id==question_id).all()
    sql_session.close()

# to get a list of dictionary answers of a question
def listAnswersDICT(question_id):
    ret_list = []
    la = listAnswers(question_id)
    print(la)
    for ans in la:
        ans_dict = ans.to_dictionary()
        ret_list.append(ans_dict)
    return ret_list

# to add a new answer
def newAnswer(answer, user_id, user_name, question_id):
    ans = Answer(question_id=question_id, answer=answer, user_id=user_id, user_name=user_name)
    try:
        sql_session.add(ans)
        sql_session.commit()
        print(ans.id)
        sql_session.close()
        return ans.id
    except Exception as e:
        print(e)
        return None