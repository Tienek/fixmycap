from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please provide a valid email address."),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=6, max=128, message="Password must be at least 6 characters.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Create Account')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data.strip().lower()).first()
        if user:
            raise ValidationError("This email address is already registered. Please log in.")


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    submit = SubmitField('Sign In')


class VehicleForm(FlaskForm):
    brand = StringField('Make / Brand', validators=[
        DataRequired(message="Vehicle brand/make is required (e.g., Toyota, Ford, BMW)."),
        Length(max=100)
    ])
    model = StringField('Model', validators=[
        DataRequired(message="Vehicle model is required (e.g., Camry, F-150, 3 Series)."),
        Length(max=100)
    ])
    year = IntegerField('Year', validators=[
        DataRequired(message="Model year is required."),
        NumberRange(min=1900, max=2030, message="Please enter a valid year between 1900 and 2030.")
    ])
    engine = StringField('Engine Details', validators=[
        DataRequired(message="Engine is required (e.g., 2.5L 4-Cyl, 3.5L V6, 2.0 TDI)."),
        Length(max=100)
    ])
    vin = StringField('VIN (Optional)', validators=[
        Optional(),
        Length(max=50, message="VIN cannot exceed 50 characters.")
    ])
    mileage = IntegerField('Current Mileage (Optional)', validators=[
        Optional(),
        NumberRange(min=0, max=2000000, message="Mileage must be positive.")
    ])
    submit = SubmitField('Save Vehicle')


class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message="Name cannot be empty."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    submit = SubmitField('Update Profile')


class StartRepairForm(FlaskForm):
    vehicle_id = SelectField('Select Vehicle', coerce=int, validators=[
        DataRequired(message="Please select a vehicle from your garage.")
    ])
    submit = SubmitField('Start Step-by-Step Repair')


class RepairNoteForm(FlaskForm):
    notes = TextAreaField('Repair Notes & Maintenance Log', validators=[
        Optional(),
        Length(max=2000, message="Notes cannot exceed 2000 characters.")
    ])
    submit = SubmitField('Save Notes')
