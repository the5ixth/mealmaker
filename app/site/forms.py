from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SubmitField, PasswordField, FieldList, DecimalField
from wtforms.validators import DataRequired, EqualTo, NumberRange

class BigForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    instructions = TextAreaField('Instructions: ', validators=[DataRequired()])
    breakfast = BooleanField('Breakfast: ', validators=[])
    lunch = BooleanField('Lunch: ', validators=[])
    dinner = BooleanField('Dinner: ', validators=[])

    ingrediants = FieldList(StringField('Ingrediant: ', validators=[]), min_entries=1, max_entries=10)
    ammounts = FieldList(StringField('Ammount: ', validators=[]), min_entries=1, max_entries=10)
    measurements = FieldList(StringField('Measurement', validators=[]), min_entries=1, max_entries=10)

    submit = SubmitField('Submit')

class SettingForm(FlaskForm):
    days = IntegerField('How many days?', validators=[DataRequired(), NumberRange(min=1, max=7)])

    breakfast = BooleanField('Breakfast: ', validators=[])
    lunch = BooleanField('Lunch: ', validators=[])
    dinner = BooleanField('Dinner: ', validators=[])

    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
	email = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	submit = SubmitField("Submit")

class SignupForm(FlaskForm):
	email = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password', validators=[DataRequired()])
	submit = SubmitField("Submit")