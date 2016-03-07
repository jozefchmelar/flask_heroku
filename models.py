from flask_heroku import app
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