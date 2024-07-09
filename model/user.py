from sqlalchemy import Column, String, Integer
from  model import Base

class User(Base):
    __tablename__ = 'users'

    id = Column("pk_user", Integer, primary_key=True)
    name = Column(String(120))
    mail = Column(String(200))

    def __init__(self, name:str, mail:str):
        self.name = name
        self.mail = mail

  
