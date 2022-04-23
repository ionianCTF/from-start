from wtforms import Form, StringField, validators

class LoginForm(Form):
    username = StringField('Username:', validators=[validators.DataRequired(), validators.Length(min=8, max=25)])
    password = StringField('Password:', validators=[validators.DataRequired(), validators.Length(min=8, max=25)])
    #email = StringField('Email:', validators=[validators.DataRequired(), validators.Length(min=0, max=50)])
