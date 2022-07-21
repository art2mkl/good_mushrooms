import wtforms
from flask import flash, session
from wtforms.validators import DataRequired
from app.models.models import User

class LoginForm(wtforms.Form):

    email = wtforms.StringField("Email",
        validators=[DataRequired()])
    password = wtforms.PasswordField("Password",
        validators=[DataRequired()])
    
    def validate(self):
        if not super(LoginForm, self).validate():
            return False
            
        self.user = User.authenticate(self.email.data, self.password.data)
        
        if not self.user:
            flash(f"Invalid email or password.", "danger")
            return False

        #Charge les paramètres de sessions
        User.load_session(self.email.data)
        return True

class RegisterForm(wtforms.Form):
    name = wtforms.StringField('Name', validators=[DataRequired()])
    email = wtforms.StringField('Email', validators=[DataRequired()])
    password = wtforms.PasswordField("Password", validators=[DataRequired()])
