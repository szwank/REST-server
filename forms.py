from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from model import User, Post


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeated_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired()])

    def validation_body(self, body):
        if len(body.data) > Post.body.property.columns[0].type.length:
            return ValidationError('Too long post. Max length is {} characters'.
                                   format(Post.body.property.columns[0].type.length))


class DropDownListOfUsers(FlaskForm):
    drop_down_list = QuerySelectField('Filter posts by usernames:', query_factory=lambda: User.query, allow_blank=False)
    submit = SubmitField('Filter')


