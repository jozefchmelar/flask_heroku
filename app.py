import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text, text, func
from sqlalchemy.orm import relationship
import re
import json
import jsonpickle 
from sqlalchemy.ext.declarative import declarative_base
# from app.models import Company


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                          'this_should_be_configured')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://nqmuwoyhdwrxjp:DllrZMcqqxw5q_swBcQQGo1G2l@ec2-54-247-170-228.eu-west-1.compute.amazonaws.com:5432/dfuidc2lc8ohah'

db = SQLAlchemy(app)

def convertToJson(object):
    json =  jsonpickle.encode(quer)    

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

    __name__ = 'Company'
    idCompany = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

    # def __repr__(self):
    #     return idCompany

    # def __dict__(self):
    #     return {
    #         'idCompany': self.idCompany, 
    #         'name': self.name,
    #      }

    def toJson(self):
        return '{"Company" : "'+ self.name +'"}' 

    def toJsonx(self):
        return json.dumps(self.__dict__(), default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)    

class User(db.Model):
    __tablename__ = 'Users'

    __name__ ='User'

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
 
    def serialize(self):
        return {
            'idUser': self.idUser, 
            'phone': self.phone,
            'name': self.name,
            'mail': str(self.mail),
            'position': self.position,
            'projects': self.projects,
         }

    def toJson(self):
        return '{ "name" : "%s" \n ",phone" : "%s" \n ",positon" : "%s" \n ",mail" : "%s}" ' % (self.name,self.phone,self.position,self.mail)
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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

    def serialize(self):
        return {
            'idProject': self.idProject, 
            'number': self.number,
            'message': self.message,
            'idCompany': self.idCompany,
            'name': self.name,
            'comment': self.comment,
            'Company': self.Company,
         }
    def toJson(self):
        return '{ "name" : "%s" \n ",number" : "%s" \n ",idCompany" : "%s" \n ",message" : "%s",comment :"%s"} ' % (self.name,self.number,self.idCompany,self.message,self.comment)


db.mapper( UserHasProject,  t_UserHasProject)


       

###
# Routing for your application.
###def toJson(self):
    #     r

def status(message):
    return '{"Status : " ' + message + '"}'

def getPersonIdByMail(mail):
    pMail = pMail.lower()
    return (User.query.filter(User.mail.ilike(pMail)))

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

@app.route('/person/all', methods=['GET'])
def getAllPersons(): 
    User.query.all()
    d=json.loads(jsonpickle.encode(select))
    for element in d: 
        del element['py/object'] 
        del element['_sa_instance_state']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    return json.dumps(d, indent=4, sort_keys=True)  

@app.route('/company/all', methods=['GET'])
def getAllCompanies(): 
    select = Company.query.all()
    d=json.loads(jsonpickle.encode(select))
    for element in d: 
        del element['py/object'] 
        del element['_sa_instance_state']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    return json.dumps(d, indent=4, sort_keys=True) 

@app.route('/project/all', methods=['GET'])
def getAllProjects(): 
    select = Project.query.all()
    d=json.loads(jsonpickle.encode(select))
    for element in d: 
        del element['py/object'] 
        del element['_sa_instance_state']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    return json.dumps(d, indent=4, sort_keys=True) 

@app.route('/person/<pMail>', methods=['GET'])
def getPersonByMail(pMail):     
    pMail = pMail.lower()
    user = User.query.filter(User.mail.ilike(pMail)).first()
    if not user:
        return render_template('404.html'), 404
    else:
        print type(company)     
        # reply =  str(user.__dict__).replace('\'','"').replace('u"','"')
        # print(reply)
        # "_sa_instance_state": <sqlalchemy.orm.state.InstanceState object at 0xb5757d2c>, 
        return jsonpickle.encode(user)
        # reply = re.sub('{"_sa_instance_state": <sqlalchemy.orm.state.InstanceState object at 0x........>, ','{',reply)
        # return reply;

@app.route('/person/<pMail>/projects', methods=['GET'])
def getPersonsProjects(pMail):
    user = User.query.filter(User.mail.ilike(pMail)).first()
    projects = user.projects
    respond = ''
    for p in projects:
        respond += p.toJson() + ' '
    return respond 
        

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
            test = UserHasProject(person.idUser,project.idProject)    
        try:       
            db.session.add(test)
            db.session.commit()
        except Exception as e :
            if re.match('.+duplicate key value.+',str(e)):
                return status('duplicate key value')
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

@app.route('/company/<pName>', methods=['GET'])
def wat(pName):
    pName = pName.lower()
    company = Company.query.filter(Company.name.ilike(pName)).first()
    if not company:
        return render_template('404.html'), 404
    else:
        print type(company)
        return company.toJson()


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

###
# The functions below should be applicable to all Flask apps.
###

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)



# thnkas to sqlacodegen
