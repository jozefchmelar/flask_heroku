import os
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify,json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import models

# from app.models import Company

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','this_should_be_configured')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# url to connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nqmuwoyhdwrxjp:DllrZMcqqxw5q_swBcQQGo1G2l@ec2-54-247-170-228.eu-west-1.compute.amazonaws.com:5432/dfuidc2lc8ohah'
#creatre new instance of sqlalchemy 
db = SQLAlchemy(app)


def status(message):
    return '{"Status : "' + message + '"}'
#this will return a query with users based on the mail.
def getPersonIdByMail(mail):
    pMail = mail.lower()
    return (models.User.query.filter(models.User.mail.ilike(pMail)))
#takes a list and returns json 
def listToJsonString(pList):
    jsonString= '['
    idNumber = 1;
    for element in pList:
        jsonString += element.toJson()+',\n'
    jsonString = jsonString[:-2] +']' 
    parsed =   json.loads(jsonString)
    return json.dumps(parsed, indent=4, sort_keys=True)  #jsonString#json.dumps(jsonString)
#      parsed = json.loads(your_json)
# >>> print json.dumps(parsed, indent=4, sort_keys=True)

# print json.dumps(jsonStr, sort_keys=True, indent=2, separators=(',', ': '))
# Routing for your application.

@app.route('/')                                                                         
def home():
    return render_template('home.html')

#checks the password via werkzeug.security package
@app.route('/login/<mail>|<password>',methods=['GET'])
def checkPassword(mail,password):
    userToCheck = getPersonIdByMail(mail).first()
    return status(str(userToCheck.check_password(password)))
                                                                            
#this will take data from forms name,mail,password etc. 
#checks for mail format, phone format  and after that it'll 
#save it into database 
@app.route('/routes/',methods=['GET'])
def routing():
    return render_template('routes.html')

@app.route('/person/', methods=['GET', 'POST'])
def person():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        toHash = request.form['password']
        position = request.form['position']
        phone = request.form['phone']
     
        if not re.match('[^@]+@[^@]+\.[^@]+', mail):
            return status('mail format error')
        
        if not re.match('[\d+]{8,}', phone):
            return status('phone format error')

        models.user = models.User(name, phone, mail, position)
        models.user.set_password(toHash)
        try:    
            db.session.add(models.user)
            db.session.commit()
            return status('true')
        except Exception:
            return status('duplicate mail')
    else:
        return render_template('person.html')

@app.route('/person/all', methods=['GET'])
def getAllPersons():  
    return listToJsonString(models.User.query.all()) 

@app.route('/company/all', methods=['GET'])
def getAllCompanies(): 
    return listToJsonString(models.Company.query.all())    

@app.route('/project/all', methods=['GET'])
def getAllProjects(): 
    return listToJsonString(models.Project.query.all())     

#return Json of person based on the mail
@app.route('/person/<pMail>', methods=['GET','POST'])
def getPersonByMail(pMail):     
    pMail = pMail.lower()
    models.user = models.User.query.filter(models.User.mail.ilike(pMail)).first()
    if models.user:
        return models.user.toJson()
    else: 
        return render_template('404.html'), 404 

@app.route('/person/byMail/',methods=['GET','POST'])
def getPersonByMailFromForm():
        pMail = request.form['mail']
        getPersonByMail(pMail)
        return getPersonByMail(pMail)

#returns all projects of the person based on persons mail.
@app.route('/person/<pMail>/projects', methods=['GET','POST'])
def getPersonsProjects(pMail):
    models.user = models.User.query.filter(models.User.mail.ilike(pMail)).first()
    projects = models.user.projects 
    return listToJsonString(projects)
          
# this will add people to project
@app.route('/AddPeople/', methods=['GET', 'POST'])
def AddPeople():
    if request.method == 'POST':   
        people = request.form['people']
        number = request.form['number']
         # in form we have more than one mail and expect it to be separted by comma
         # this will split everything into list based on the comma in form.
        listPeople = re.split(',',people)
        # check all mails.
        for email in listPeople:
            if not re.match('[^@]+@[^@]+\.[^@]+', email):
                return status('mail format error') 
        else: 
            #find project based on number
            models.project = (models.Project.query.filter(models.Project.number.ilike(number))).first()    
            #go through emails in list and add data to session and after that commit it into db
            for email in listPeople:    
                models.person = getPersonIdByMail(email).first() 
                test = models.UserHasProject(models.person.idUser,models.project.idProject)   
                db.session.add(test) 
        try:       
            #db.session.add(test)
            db.session.commit()
        except Exception as e :
            if re.match('.+duplicate key value.+',str(e)):
                return status('duplicate key value '+str(e))
        return status('true')
    else:
        return render_template('addPeopleToProject.html')

@app.route('/project/', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']        
        nameOfTheCompany = request.form['nameOfTheCompany']          
        message = request.form['message']
        comment =  request.form['comment']            
         #based on the name of the company find it's Id
        companyid =  (models.Company.query.filter(models.Company.name.ilike(nameOfTheCompany)).first()).idCompany   
        #number has to be 4 digit number.
        if not re.match('[0-9]{4}', number): 
            return status('wrong number format')
        else:        
            project = models.Project(number,companyid,name,message,comment)
        try:
            db.session.add(project) 
            db.session.commit()
            return status('true')
        except Exception:
            return status('false')
    else:
        return render_template('project.html')

@app.route('/project/<number>/users', methods=['GET', 'POST'])
def getProjectUsers(number):
    models.project = (models.Project.query.filter(models.Project.number.ilike(number))).first()
    usersInProject = models.project.users    
    return listToJsonString(usersInProject) 

@app.route('/company/', methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        companyName = request.form['companyName']
        models.company = models.Company(companyName)
        try:
            db.session.add(models.company)
            db.session.commit()
            return status('true')
        except Exception:
            return status('false')
    else:
        return render_template('company.html')

@app.route('/company/<pName>', methods=['GET'])
def wat(pName):
    pName = pName.lower()
    models.company =  models.Company.query.filter(Company.name.ilike(pName)).first()
    if not company:
        return render_template('404.htm l'), 404
    else:
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