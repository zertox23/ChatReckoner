from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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
        voted_user = Column("voted_user",Integer,ForeignKey("members.id"))
        upvotes    = Column("upvotes",Integer)
        downvotes  = Column("upvotes",Integer)
    
class BotDb:
    def __init__(self) -> None: 
        engine = create_engine("sqlite:///database/databse.db")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
