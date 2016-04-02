from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text, text, func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, \
     check_password_hash 
import jsonpickle
from flask import json
from app  import db 

class UserHasProject(object):
    def __init__(self,idUser,idProject):
        self.idUser=idUser
        self.idProject=idProject

t_UserHasProject = db.Table(
    'UserHasProject', db.metadata,
    db.Column('idUser',db.Integer, db.ForeignKey('Users.idUser'), primary_key=True, nullable=False),
    db.Column('idProject',db.Integer, db.ForeignKey('Projects.idProject'), primary_key=True, nullable=False)
)

    
class User(db.Model):
    __tablename__ = 'Users'
    __name__ ='User'

    idUser = db.Column(Integer, primary_key=True, unique=True)
    phone  = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    position = db.Column(db.String(30))
    mail = db.Column(db.String(50), nullable=False, unique=True) 
    password = db.Column(db.String(16), nullable=False)  
    projects = db.relationship("Project",
            secondary=t_UserHasProject,
            backref=db.backref("users", lazy="dynamic"),
            )
    #password hashing
    def set_password(self, toHash):
        self.password = generate_password_hash(toHash)
    #password hashing
    def check_password(self, hashed):
        return check_password_hash(self.password, hashed)

    def __init__(self, name, phone, mail, position):
        self.name = name.lower()
        self.phone = phone
        self.mail = mail.lower()
        self.position = position.lower()    

    #this is very important to jsonpickle.        
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        del state['password']
        return state

    #this is very important to jsonpickle.
    def __setstate__(self, state):
        self.__dict__.update(state)

    def toJson(self):
        return jsonpickle.encode(self, unpicklable=False)    

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

    #this is very important to jsonpickle.     
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        return state
    #this is very important to jsonpickle.        
    def __setstate__(self, state):
        self.__dict__.update(state)
    
    def toJson(self):
        return jsonpickle.encode(self, unpicklable=False)


class Company(db.Model):
    __tablename__ = 'Company'
    __name__ = 'Company'

    idCompany = db.Column(db.Integer, primary_key=True,server_default=text("nextval('seqproject'::regclass)"))
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

    def toJson(self):             
        return '{"idCompany" :"'+ str(self.idCompany) +'",\n "name" : "'+self.name+'"}\n'
        
#imporatnt to map the relationship.
db.mapper(UserHasProject,t_UserHasProject)
