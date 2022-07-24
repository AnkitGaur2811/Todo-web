# Importing Flask's form modules to make the forms
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import InputRequired, Email, EqualTo,Length
from wtforms.widgets import TextArea

# we have to make class for each form

#--------------------------------------- User login form -----------------------------------------
class loginform(FlaskForm):
    email = StringField("Email", validators=[InputRequired(),Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

#---------------------------------------- User Registration form ----------------------------------
class signupform(FlaskForm):
    fullname = StringField("Name", validators=[InputRequired()],description="Enter Your full name here")
    email = StringField("Email", validators=[InputRequired(), Email()],description="Enter Your email ID here")
    phone = StringField("Phone", validators=[InputRequired(),Length(min=8,max=10, message="Entered phone number can't exist")],description="Enter Your phone number")
    password = PasswordField('Password', validators = [InputRequired()],description="Enter the password kindly remeber it only made once")
    confirm_password = PasswordField('Confirm Password',validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

#------------------------------------------------ Create Task form -----------------------------------
class createtaskform(FlaskForm):
    title = StringField("Title fo New Task",validators=[InputRequired()],description="Choose tittle carefully this tasks will be known by title")
    desc=StringField("Description for the task", widget=TextArea())
    status=SelectField("Status of Task",choices=["Incomplete","Inprogress","Done"],validate_choice=True,default=3)
    submit = SubmitField('Create Task')

#-------------------------------------------------------- Update Task Form ---------------------------------------

class updatetaskform(FlaskForm):
    title = StringField("Title fo New Task",validators=[InputRequired()],description="Choose tittle carefully this tasks will be known by title")
    desc=StringField("Description for the task")
    status=SelectField("Status of Task",choices=["Incomplete","Inprogress","Done"],validate_choice=True,default=3)
    submit = SubmitField('Update Task')


