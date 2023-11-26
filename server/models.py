from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

animal_enclosure = db.Table(
    'animal_enclosure',
    db.Column('animal_id', db.Integer, db.ForeignKey('animals.id')),
    db.Column('enclosure_id', db.Integer, db.ForeignKey('enclosures.id'))
)

class Zookeeper(db.Model):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthday = db.Column(db.DateTime)

    # Define the relationship with a different backref name
    animals = db.relationship('Animal', backref='zookeeper', lazy=True)

class Enclosure(db.Model):
    __tablename__ = 'enclosures'

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean, default=False)
    
    # Define the relationship
    animals = db.relationship('Animal', secondary=animal_enclosure, back_populates='enclosures')

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)
    enclosure = db.Column(db.Boolean, default=False)
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    

    zookeeper = db.relationship('Zookeeper', back_populates='animals')
    enclosures = db.relationship('Enclosure', secondary=animal_enclosure, back_populates='animals')
