from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import datetime
from os import path

# SQL access layer initialization
DATABASE_FILE = "Videos.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Video(Base):
    __tablename__ = 'Video'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    url = Column(String)
    views = Column(Integer, default = 0)

    def __repr__(self):
        return "<YouTubeVideo (id=%d Description=%s, URL=%s, Views=%s>" % (self.id, self.description, self.url,  self.views)

    def to_dictionary(self):
        return {"video_id": self.id, "description": self.description, "url": self.url, "views": self.views}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
sql_session = scoped_session(Session)
# session = Session()


def listVideos():
    return sql_session.query(Video).all()
    sql_session.close()

def listVideosDICT():
    ret_list = []
    lv = listVideos()
    print(lv)
    for v in lv:
        vd = v.to_dictionary()
        del(vd["url"])
        del(vd["views"])
        ret_list.append(vd)
    return ret_list

def getVideo(id):
    v =  sql_session.query(Video).filter(Video.id==id).first()
    sql_session.close()
    return v

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