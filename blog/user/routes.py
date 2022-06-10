
from datetime import datetime
import os
import shutil

from flask_login import current_user, login_required, logout_user, login_user


from blog.models import User
from blog import bcrypt, db
from flask import Blueprint, flash, redirect, render_template, url_for, request
from blog.user.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


# Маршрут для регистрации
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = RegistrationForm()
    # Проверка валидации
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        # создания пути где будет папка с данными пользователя
        full_path = os.path.join(os.getcwd(), 'blog/static', 'profile_pics', user.username)
        # Если папки нет то зоздать
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        
        shutil.copy(f"{os.getcwd()}/blog/static/profile_pics/default.jpg", full_path)
        flash("Ваш акаунт был создан. Вы можете войти в блог", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title="Регистрация", legend="Регистрация")

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = LoginForm()
    # если форма проходит валидацию получить юзера с уникально почтой
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # если условие True тогда логиним пользователя
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вы вошли как пользователь {current_user.username}', 'info')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Войти не удалось. Пожалуйста, проверте электронну почту или пароль', 'danger')
    
    return render_template('login.html', form=form, title="Авторизация", legend="Войти")



@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html')


@users.route('/logout')
def logout():
    current_user.last_seen = datetime.now()
    db.session.commit()
    logout_user()
    return redirect(url_for('main.home'))
