from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField, FieldList
from wtforms.validators import DataRequired, EqualTo

class BigForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    instructions = TextAreaField('Instructions: ', validators=[DataRequired()])

    ingrediants = FieldList(StringField('Ingrediant: ', validators=[DataRequired()]), min_entries=1, max_entries=10)
    ammounts = FieldList(IntegerField('Ammount: ', validators=[DataRequired()]), min_entries=1, max_entries=10)
    measurements = FieldList(StringField('Measurement', validators=[DataRequired()]), min_entries=1, max_entries=10)

    submit = SubmitField('Submit')