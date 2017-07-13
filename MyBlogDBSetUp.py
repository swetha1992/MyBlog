import sys
from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base=declarative_base()



class Login(Base):
	__tablename__='login'

	username=Column(String(50),nullable=False,primary_key=True)
	password=Column(String(50),nullable=False)
	email=Column(String(50),nullable=False)

	

	
class MyBlog(Base):
	__tablename__='myblog'

	username=Column(String(50),nullable=False)
	date=Column(String(50),nullable=False)
	blogcontent=Column(String(200),nullable=False,primary_key=True)

	
	


engine=create_engine('sqlite:///myblog.db')
Base.metadata.create_all(engine)
