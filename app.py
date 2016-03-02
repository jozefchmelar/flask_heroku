"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                          'this_should_be_configured')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)



###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


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
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)




Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'Company'

    idCompany = Column(BigInteger, primary_key=True)
    name = Column(String(30))


class Project(Base):
    __tablename__ = 'Projects'

    idProject = Column(BigInteger, primary_key=True)
    number = Column(String(20), nullable=False)
    message = Column(Text)
    idCompany = Column(ForeignKey(u'Company.idCompany'), nullable=False, index=True)
    name = Column(String(30))
    comment = Column(String(200))

    Company = relationship(u'Company')
    Users = relationship(u'User', secondary='UserHasProject')


t_UserHasProject = Table(
    'UserHasProject', metadata,
    Column('idUser', ForeignKey(u'Users.idUser'), primary_key=True, nullable=False),
    Column('idProject', ForeignKey(u'Projects.idProject'), primary_key=True, nullable=False)
)


class User(Base):
    __tablename__ = 'Users'

    idUser = Column(Integer, primary_key=True, unique=True)
    phone = Column(String(20), nullable=False)
    name = Column(String(40), nullable=False)
    position = Column(String(30))
    mail = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    name = Column(String(80))
    email = Column(String(120), unique=True)
