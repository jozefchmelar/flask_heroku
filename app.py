import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text, text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                          'this_should_be_configured')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://nqmuwoyhdwrxjp:DllrZMcqqxw5q_swBcQQGo1G2l@ec2-54-247-170-228.eu-west-1.compute.amazonaws.com:5432/dfuidc2lc8ohah'
db = SQLAlchemy(app)


class Company(db.Model):
    __tablename__ = 'Company'

    idCompany = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Name %r>' % self.name

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/company/')
def company():
    """Render website's home page."""
    return render_template('company.html')


@app.route('/company/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    company = Company(text)
    try:
	    db.session.add(company)
	    db.session.commit()    
	    return '{"status":"true"}'
    except Exception:
	    return '{"status":"false"}'		



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


@app.route('/company/<pName>', methods=['GET'])
def wat(pName):
    pName = pName.lower()
    company = Company.query.filter(Company.name.ilike(pName)).first()
    if not company:
        return render_template('404.html'), 404
    else:
        print type(company)
        return company.name


if __name__ == '__main__':
    app.run(debug=True)
# thnkas to sqlacodegen
