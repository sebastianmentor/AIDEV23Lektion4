from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import IntegerField, SelectField, SubmitField, StringField
from models import Person

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

class RegisterNewPersonForm(FlaskForm):
    name = StringField('Namn', [validators.DataRequired(), validators.Length(2, 40, message='Måste vara mellan 2 och 40 karaktärer!')])
    age = IntegerField('Ålder', [validators.NumberRange(1, 120, message='Du få inte vara yngre än 1 år eller äldre än 120!')])
    phone = StringField('Telefonnummer', [validators.InputRequired(message='Har du inget telefonnummer?')])
    email = StringField('Epost', [validators.Email(message='Helt fel format!'), check_if_email_is_valid_and_not_used])
    username = StringField('Användarnamn', [validators.DataRequired(), check_if_username_is_valid_and_not_used])
    submit = SubmitField('Skapa')


        # name = request.form.get('name')
        # age = request.form.get('age',type=int)
        # email = request.form.get('email')
        # username = request.form.get('username')
        # phone = request.form.get('phone')