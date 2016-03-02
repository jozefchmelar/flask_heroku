from app import db

class Company(db.Model):
    __tablename__ = 'Company'

    idCompany = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Name %r>' % self.name
