from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Некоректний емейл')])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField('Запам`ятати', default=False)
    submit = SubmitField('Увійти')


class RegisterForm(FlaskForm):
    name = StringField('Ім`я: ', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email: ', validators=[Email('Некоректний емейл')])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100)])
    password2 = PasswordField('Повтор пароля: ', validators=[DataRequired(), EqualTo('password', message='Паролі не співпадають')])
    submit = SubmitField('Реєстація')
