
from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, hash_password
from faker import Faker
import random
import datetime

db = SQLAlchemy()

# Definiera modeller för användare och roller
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

# Sätt upp Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)
    email = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(128), unique = True)
    phone = db.Column(db.String(128))

def seed_data():

    if not Role.query.first():
        user_datastore.create_role(name='Admin')
        user_datastore.create_role(name='User')
        db.session.commit()

    if not User.query.first():
        user_datastore.create_user(email='test@example.com', password=hash_password('password'), roles=['Admin','User'], confirmed_at=datetime.datetime.now())
        user_datastore.create_user(email='c@c.com', password=hash_password('password'), roles=['User'] ,confirmed_at=datetime.datetime.now())
        user_datastore.create_user(email='d@d.com', password=hash_password('password'), roles=['Admin'], confirmed_at=datetime.datetime.now())
        db.session.commit()
        
    faker = Faker()
    while Person.query.count() < 500:
        new_name = faker.name()
        new_age = random.randint(20, 100)

        new_email = faker.email()
        while Person.query.filter_by(email=new_email).first():
            new_email = faker.email()

        new_username = faker.user_name()
        while Person.query.filter_by(username=new_username).first():
            new_username = faker.user_name()

        new_phone = str(random.randint(10000000,99999999))
        
        new_user = Person(name=new_name, age=new_age,email=new_email, username=new_username, phone=new_phone)
        db.session.add(new_user)
        db.session.commit()

