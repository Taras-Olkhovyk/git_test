from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email

# форма для аторизации пользователя
class LoginForm(FlaskForm):
    email = StringField('Емайл', validators=[DataRequired(), Email()])  # проверка на данные и правельность емейла
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


