from sqlalchemy import create_engine, ForeignKey, Column, String, Integer,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

global base
Base = declarative_base()

class DbStruct:        

    class member(Base):
        __tablename__ = "members"
        user_id = Column("user_id", Integer, primary_key=True)
        username = Column(
            "username",
            String,
        )
        rank = Column("rank", String)
        votes = Column("votes", Integer)
        messages_sent = Column("messages_sent", Integer)

        def __init__(
            self, user_id: int, username: str, rank: str, votes: int, messages_sent: int):
            self.user_id = user_id
            self.username = username
            self.rank = rank
            self.votes = votes
            self.messages_sent = messages_sent

        def __repr__(self):
            return str({
                "user_id": self.user_id,
                "username": self.username,
                "rank": self.rank,
                "votes": self.votes,
                "messages_sent": self.messages_sent,
            })
    
    class tierpolls(Base):
        __tablename__ = "tierpolls"

        id = Column("id",String,primary_key=True) # message link
        submitted_by = Column("submitted_by", Integer, ForeignKey("members.user_id"))
        voted_user = Column("voted_user",Integer,ForeignKey("members.user_id"))
        votes    = Column("votes",Integer)
        upvotes = Column("upvotes",Integer)
        downvotes = Column("downvotes",Integer)
        last_recorded = Column("last_recorded",Integer)

        def __init__(self,message_id:str,submitted_by:int,voted_user:int):
            self.id = message_id
            self.votes = 0
            self.submitted_by = submitted_by
            self.voted_user = voted_user
            self.last_recorded = 0
            self.downvotes = 0
            self.upvotes = 0
        def __repr__(self):
            return str({
                "id":self.id,
                "votes":self.votes,
                "submitted_by":self.submitted_by,
                "last_recorded":self.last_recorded,
                "voted_user":self.voted_user,
                "upvotes": self.upvotes,
                "downvotes": self.downvotes
            })

    class discussion_ideas(Base):
        __tablename__ = "discussion_ideas"
        id       = Column("id", String, primary_key=True)  # message link
        votes    = Column("votes",Integer)
        upvotes = Column("upvotes",Integer)
        downvotes = Column("downvotes",Integer)
        submitted_by = Column("submitted_by",Integer,ForeignKey("members.user_id"))
        submittion_date = Column("submission_date", DateTime, default=datetime.datetime.utcnow)

        def __init__(self,id:str,submitted_by:int,votes:int=0):
            self.id = id
            self.submitted_by = submitted_by
            self.votes = votes
            self.downvotes = 0
            self.upvotes = 0

        def __repr__(self):
            return str({
                "id": self.id,
                "votes": self.votes,
                "submitted_by":self.submitted_by,
                "submission_date": self.submittion_date,
                "upvotes": self.upvotes,
                "downvotes": self.downvotes
            })

    
class BotDb:
    def __init__(self) -> None: 
        engine = create_engine("sqlite:///database.db")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
