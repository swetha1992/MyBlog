from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import inspect
from MyBlogDBSetUp import Login,Base,MyBlog

import datetime
engine=create_engine('sqlite:///myblog.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


app=Flask(__name__)

userdetails=session.query(Login).all()
usernamelist=[]
passwordlist=[]
emaillist=[]
blogusernamelist=[]
bloglist=[]
datelist=[]
usernamePassworddict={}
currentuser=""
blogdetails=session.query(MyBlog).all()

for user in userdetails:
  usernamePassworddict[user.username]=user.password
  usernamelist.append(user.username)
  passwordlist.append(user.password)
  emaillist.append(user.email)

count=len(usernamelist)

for blog in blogdetails:

  blogusernamelist.append(blog.username)
  bloglist.append(blog.blogcontent)
  datelist.append(blog.date)

blogcount=len(blogusernamelist)

@app.route('/mybloglogin', methods=['GET','POST'])
def MyBlogLogin(): 
  if(request.method=='POST'):
    username=request.form['username']
    password=request.form['password']
    if(username in usernamePassworddict and usernamePassworddict[username]==password):
      datelist=[]
      bloglist=[]
      for blog in blogdetails:
        if(blog.username==username):
          datelist.append(blog.date);
          bloglist.append(blog.blogcontent)

      currentuser=username
      blogcount=len(bloglist)
      return render_template('/mybloghome.html',username=currentuser,datelist=datelist,bloglist=bloglist,blogcount=blogcount)
    else:
      return render_template('MyBlogLogin.html',error='Invalid Username or Password')
  else:  
    return render_template('MyBlogLogin.html')
        
@app.route('/myblognewuser', methods=['GET','POST'])
def MyBlogNewUser():
  if request.method=='POST':
    session = DBSession()
    message=""
    username=request.form['username']
    password=request.form['password']
    email=request.form['email']
    try:
      user=Login(username=username,password=password,email=email)
      session.add(user)
      session.commit()
      success=True
    except :
      return render_template('MyBlogNewUser.html',message='We are not able to add your details')
      success=False
    if(success==True):
      return render_template('MyBlogNewUser.html',message='registered successfully')
    else:
      return render_template('MyBlogNewUser.html',message='We are not able to add your details') 
  else :
     return render_template('MyBlogNewUser.html')

@app.route('/mybloghome', methods=['GET','POST'])
def MyBlogHome():
  if request.method=='POST':
    session = DBSession()
    message=""
    blogcontent=request.form['blogcontent']
    date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    username=currentuser

    datelist=[]
    bloglist=[]
    for blog in blogdetails:
        if(blog.username==username):
          datelist.append(blog.date);
          bloglist.append(blog.blogcontent)
    blogcount=len(bloglist)
    try:
      user=MyBlog(username=username,date=date,blogcontent=blogcontent)
      session.add(user)
      session.commit()
      success=True
    except Exception as e:
      success=False
    if(success==True):
      return render_template('MyBlogHome.html',username=currentuser,message='blog added succesfully',datelist=datelist,bloglist=bloglist,blogcount=blogcount)
    else:
      return render_template('MyBlogHome.html',username=currentuser,message='could not add your blog',datelist=datelist,bloglist=bloglist,blogcount=blogcount)
  else :
    return render_template('MyBlogHome.html',username=currentuser,datelist=datelist,bloglist=bloglist,blogcount=blogcount) 
  
@app.route('/myblogtabledetails', methods=['GET','POST'])
def MyBlogTableDetails():
    return render_template('MyBlogTableDetails.html',usernamelist=usernamelist,passwordlist=passwordlist,emaillist=emaillist, count=count,blogusernamelist=blogusernamelist,bloglist=bloglist,datelist=datelist,blogcount=blogcount)
if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=8000)

