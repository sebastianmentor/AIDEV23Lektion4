from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import IntegerField, SelectField, SubmitField, StringField, PasswordField
from models import Person, User


#---------------------Persons----------------------------
def check_if_Person_email_exist_in_database(email:str) -> bool:
    return True if  Person.query.where(Person.email==email).first() else False

def check_if_Person_username_exist_in_database(username:str) -> bool:
    return True if  Person.query.where(Person.username==username).first() else False

def check_if_email_is_valid_and_not_used(form, field):
    if check_if_Person_email_exist_in_database(field.data):
        raise ValidationError('Email already exist!')
    
def check_if_username_is_valid_and_not_used(form, field):
    if check_if_Person_username_exist_in_database(field.data):
        raise ValidationError('Username already exist!')
    
#---------------------USER----------------------------    
def check_if_User_email_exist_in_database(email:str) -> bool:
    return True if  User.query.where(User.email==email).first() else False
    
def check_if_user_email_is_valid_and_not_used(form, field):
    if check_if_Person_username_exist_in_database(field.data):
        raise ValidationError('Username already exist!')

class RegisterNewPersonForm(FlaskForm):
    name = StringField('Namn', [validators.Length(2, 40, message='Måste vara mellan 2 och 40 karaktärer!')])
    age = IntegerField('Ålder', [validators.NumberRange(1, 120, message='Du få inte vara yngre än 1 år eller äldre än 120!')])
    phone = StringField('Telefonnummer', [validators.InputRequired(message='Har du inget telefonnummer?')])
    email = StringField('Epost', [validators.Email(message='Helt fel format!'), check_if_email_is_valid_and_not_used])
    username = StringField('Användarnamn', [validators.DataRequired(), check_if_username_is_valid_and_not_used])
    submit = SubmitField('Skapa')

class RegisterNewUserForm(FlaskForm):
    email = StringField('Epost', [validators.DataRequired(), check_if_user_email_is_valid_and_not_used])
    password = PasswordField('Lösenord', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Måste vara samma lösenord!')
    ])
    confirm = PasswordField('Repetera Lösenord')
    roles = SelectField('Roll', choices=[('Admin', 'admin'), ('User', 'user'), ('Superuser', 'superuser')])
    submit = SubmitField('Registrera')

    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(100), unique=True)
    # password = db.Column(db.String(100))
    # active = db.Column(db.Boolean())
    # fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    # confirmed_at = db.Column(db.DateTime())
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))