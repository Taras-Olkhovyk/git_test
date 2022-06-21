from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from blog.models import User
from flask_wtf.file import FileAllowed

# форма для аторизации пользователя
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Емайл', validators=[DataRequired(), Email()])  # проверка на данные и правельность емейла
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Войти')
    
    def valodate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Это имя уже занятою Пожалуйста, выберите другое', 'danger')
            raise ValidationError('That username is taken. Please choose a different one')
        
    
    def valodate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Этот емейл уже занят Пожалуйста, выберите другой', 'danger')
            raise ValidationError('That email is taken. Please choose a different one')
        
        
# форма для аторизации пользователя
class LoginForm(FlaskForm):
    email = StringField('Емайл', validators=[DataRequired(), Email()])  # проверка на данные и правельность емейла
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Емейл', validators=[DataRequired(), Email()])    
    picture = FileField('Изображение (png, jpg)', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')
    
    
    def valodate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash('Это имя уже занятою Пожалуйста, выберите другое', 'danger')
                raise ValidationError('That username is taken. Please choose a different one')
        
    
    def valodate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('Этот емейл уже занят Пожалуйста, выберите другой', 'danger')
                raise ValidationError('That email is taken. Please choose a different one')
            