from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "ytVideos.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class YTVideo(Base):
    __tablename__ = 'YTVideo'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    url = Column(String)
    views = Column(Integer, default = 0)
    def __repr__(self):
        return "<YouTubeVideo (id=%d Description=%s, URL=%s, Views=%s>" % (
                                self.id, self.description, self.url,  self.views)
    def to_dictionary(self):
        return {"video_id": self.id, "description": self.description, "url": self.url, "views": self.views}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listVideos():
    return session.query(YTVideo).all()
    session.close()

def listVideosDICT():
    ret_list = []
    lv = listVideos()
    for v in lv:
        vd = v.to_dictionary()
        del(vd["url"])
        del(vd["views"])
        ret_list.append(vd)
    return ret_list

def getVideo(id):
     v =  session.query(YTVideo).filter(YTVideo.id==id).first()
     session.close()
     return v

def getVideoDICT(id):
    return getVideo(id).to_dictionary()

def newVideoView(id):
    b = session.query(YTVideo).filter(YTVideo.id==id).first()
    b.views+=1
    n = b.views
    session.commit()
    session.close()
    return n


def newVideo(description , url):
    vid = YTVideo(description = description, url = url)
    try:
        session.add(vid)
        session.commit()
        print(vid.id)
        session.close()
        return vid.id
    except:
        return None



if __name__ == "__main__":
    pass