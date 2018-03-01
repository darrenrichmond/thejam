from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, URL, Length
from app.models import User

#This form allows a user to log in
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#This form allows a user to register wtih the site.
#This allows them to set their home address on their profile,
#which will allow them to get drive times
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please enter a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please enter a different email address.')

#This form allows the user to set or update their profile
#This allows them to set their home address on their profile,
#which will allow them to get drive times
class ProfileForm(FlaskForm):
    address = StringField('Home Address', validators=[DataRequired()])
    submit = SubmitField('Update')

#This is a common form for creating and editing events
class CreateEditEventForm(FlaskForm):
    venue_name = StringField('Venue Name', validators=[DataRequired()])
    venue_address = StringField('Venue Address')
    venue_website = StringField('Venue Website')
    event_night = StringField('Event Night', validators=[DataRequired()])
    event_recurs = StringField('Event Recurrence')
    event_start = StringField('Event Start Time', validators=[DataRequired()])
    event_end = StringField('Event End Time', validators=[DataRequired()])
    event_adv_signup = StringField('Advanced Signup Time')
    event_notes = TextAreaField('Notes', validators=[Length(max=120)])
    submit = SubmitField('Update')