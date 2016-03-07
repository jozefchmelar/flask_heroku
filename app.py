import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text, text, func
from sqlalchemy.orm import relationship
import re
from sqlalchemy.ext.declarative import declarative_base
# from app.models import Company

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                          'this_should_be_configured')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://nqmuwoyhdwrxjp:DllrZMcqqxw5q_swBcQQGo1G2l@ec2-54-247-170-228.eu-west-1.compute.amazonaws.com:5432/dfuidc2lc8ohah'

db = SQLAlchemy(app)


class UserHasProject(object):
    def __init__(self,idUser,idProject):
        self.idUser=idUser
        self.idProject=idProject
t_UserHasProject = db.Table(
    'UserHasProject', db.metadata,
    db.Column('idUser',db.Integer, db.ForeignKey('Users.idUser'), primary_key=True, nullable=False),
    db.Column('idProject',db.Integer, db.ForeignKey('Projects.idProject'), primary_key=True, nullable=False)
)
class Company(db.Model):
    __tablename__ = 'Company'
    idCompany = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return idCompany
    def toJson(self):
        return '{"Company" : "'+ self.name +'"}'      

class User(db.Model):
    __tablename__ = 'Users'

    idUser = db.Column(Integer, primary_key=True, unique=True)
    phone  = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    position = db.Column(db.String(30))
    mail = db.Column(db.String(50), nullable=False, unique=True)     
    projects = db.relationship("Project",
            secondary=t_UserHasProject,
            backref=db.backref("users", lazy="dynamic"),
            )
    def __init__(self, name, phone, mail, position):
        self.name = name.lower()
        self.phone = phone
        self.mail = mail.lower()
        self.position = position.lower()

    def __repr__(self):
        return '<mail %r>' % self.mail

    def toJson(self):
        return '{ "name" : "%s" \n ",phone" : "%s" \n ",positon" : "%s" \n ",mail" : "%s}" ' % (self.name,self.phone,self.position,self.mail)

class Project(db.Model):
    __tablename__ = 'Projects'

    idProject = db.Column(db.BigInteger, primary_key=True, server_default=text("nextval('seqproject'::regclass)"))
    number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text)
    idCompany = db.Column(db.ForeignKey('Company.idCompany'), nullable=False, index=True)
    name = db.Column(db.String(30))
    comment = db.Column(db.String(200))
    Company = db.relationship('Company')
   

    def __init__(self, number, idCompany, name, message,comment):
        self.name = name.lower()
        self.number = number
        self.idCompany = idCompany
        self.message = message 
        self.comment=comment
    def toJson(self):
        return '{ "name" : "%s" \n ",number" : "%s" \n ",idCompany" : "%s" \n ",message" : "%s",comment :"%s"} ' % (self.name,self.number,self.idCompany,self.message,self.comment)


db.mapper( UserHasProject,  t_UserHasProject)


       

###
# Routing for your application.
###

def status(message):
    return '{"Status : " ' + message + '"}'

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
  
@app.route('/person/', methods=['GET', 'POST'])
def person():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        if not re.match('[^@]+@[^@]+\.[^@]+', mail):
            return status('mail format error')
        position = request.form['position']
        phone = request.form['phone']
        if not re.match('[\d+]{8,}', phone):
            return status('phone format error')
        user = User(name, phone, mail, position)
        try:
            db.session.add(user)
            db.session.commit()
            return status('true')
        except Exception:
            return status('duplicate mail')
    else:
        return render_template('person.html')

  
@app.route('/person/<pMail>', methods=['GET'])
def getPersonByMail(pMail):     
    pMail = pMail.lower()
    user = User.query.filter(User.mail.ilike(pMail)).first()
    if not user:
        return render_template('404.html'), 404
    else:
        print type(company)
        return user.toJson() 

def getPersonIdByMail(mail):
    pMail = pMail.lower()
    return (User.query.filter(User.mail.ilike(pMail)).first())

# addPeopleToProject
@app.route('/AddPeople/', methods=['GET', 'POST'])
def AddPeople():
    if request.method == 'POST':   
        poeple = request.form['people']
        number = request.form['number']
        listPeople = re.split(',',poeple)
        for email in listPeople:
            if not re.match('[^@]+@[^@]+\.[^@]+', email):
                return status('mail format error') 
        else:
            person =  (User.query.filter(User.mail.ilike(email))).first()
            project = (Project.query.filter(Project.number.ilike(number))).first()
            print('aaaaaaaaaapppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppaaaaaaaahoooooooj')
            print(project.number)
            print type(project)
            print (person)
            print type(person)
            test = UserHasProject(person.idUser,project.idProject) 
          
            db.session.add(test)
            db.session.commit()
            # db.session.add(UserHasProject(getPersonByMail(email),number))

        return status('true')
    else:
        return render_template('addPeopleToProject.html')
@app.route('/project/', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']        
        nameOfTheCompany = request.form['nameOfTheCompany']         
        companyid =  (Company.query.filter(Company.name.ilike(nameOfTheCompany)).first()).idCompany     
        message = request.form['message']
        comment =  request.form['comment']            
        if not re.match('[1-9]{4}', number): 
            return status('wrong number format')
        else:        
            project = Project(number,companyid,name,message,comment)
        try:
            db.session.add(project) 
            db.session.commit()
            return status('true')
        except Exception:
            return status('false')
    else:
        return render_template('project.html')


@app.route('/company/', methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        companyName = request.form['companyName']
        company = Company(companyName)
        try:
            db.session.add(company)
            db.session.commit()
            return status('true')
        except Exception:
            return status('false')
    else:
        return render_template('company.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/company/<pName>', methods=['GET'])
def wat(pName):
    pName = pName.lower()
    company = Company.query.filter(Company.name.ilike(pName)).first()
    if not company:
        return render_template('404.html'), 404
    else:
        print type(company)
        return company.toJson()

if __name__ == '__main__':
    app.run(debug=True)
# thnkas to sqlacodegen
