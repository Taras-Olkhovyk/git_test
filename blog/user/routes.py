
from crypt import methods
from datetime import datetime
import os
import shutil
from urllib.parse import uses_relative

from flask_login import current_user, login_required, logout_user, login_user
import sqlalchemy
from blog.models import Post, User
from blog import bcrypt, db
from flask import Blueprint, flash, redirect, render_template, url_for, request
from blog.post.routes import post
from blog.user.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog.user.utils import save_picture, random_avatar



users = Blueprint('user', __name__, template_folder='templates')


# Маршрут для регистрации
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = RegistrationForm()
    # Проверка валидации
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file=random_avatar(form.username.data))
        db.session.add(user)
        db.session.commit()           
                
        flash("Ваш акаунт был создан. Вы можете войти в блог", 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form, title="Регистрация", legend="Регистрация")

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
            return redirect(next_page) if next_page else redirect(url_for('user.account'))
        else:
            flash('Войти не удалось. Пожалуйста, проверте электронну почту или пароль', 'danger')
    
    return render_template('user/login.html', form=form, title="Авторизация", legend="Войти")


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)

    return render_template('user/user_posts.html', title='Блог>', posts=posts, user=user)

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # получаєм поьзователя и берем его имя
    user = User.query.filter_by(username=current_user.username).first()
    # собераем все посты
    posts = Post.query.all()
    # берем всег пользователей
    users = User.query.all()
    # подключаем форму обновления аккаунта
    form = UpdateAccountForm()
    
    if request.method == 'GET':
        # имя пользователя емейл предаются в форму для обработки
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    elif form.validate_on_submit():
        path_one = os.path.join(os.getcwd(), f'blog/static/profile_pics/{user.username}')
        path_two = os.path.join(os.getcwd(), f'blog/static/profile_pics/{form.username.data}')
        os.rename(path_one, path_two)
        current_user.username = form.username.data
        current_user.email = form.email.data
        # если кнопка нажата обрезать фото если нет оставить текущей
        # проверка для формы изображения
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        else:
            form.picture.data = current_user.image_file
        
        db.session.commit()
        flash('Ваш аккаунт был обновлён!', 'success')
        return redirect(url_for('user.account'))
    image_file = url_for('static', filename=f'profile_pics/' + current_user.username + '/account_image/'
                            + current_user.image_file)
    
    return render_template('user/account.html', user=user, title='Аккаунт', users=users, posts=posts, image_file=image_file, form=form)





# функцыя удаления пользователя 
@users.route('/delete_user/<string:username>', methods=['GET', 'POST'])
@login_required
def delete_user(username):
    try:
        user = User.query.filter_by(username=username).first_or_404()
        # проверяем не является ли пользователь админом
        if user and user.username != 'Taras':
            db.session.delete(user)
            db.session.commit()
            full_path = os.path.join(os.getcwd(), 'blog/static', 'profile_pics', user.username)
            print(full_path)
            shutil.rmtree(full_path)

            flash(f'Пользователь {username} был удалён!', 'info')
            return redirect(url_for('user.account'))
        
    except sqlalchemy.exc.IntegrityError:
        flash(f'У пользователя {username} есть контент!', 'warning')
        return redirect(url_for('user.account'))

    else:
        flash('Администрация!', 'info')
        return redirect(url_for('user.account'))


@users.route('/logout')
def logout():
    current_user.last_seen = datetime.now()
    db.session.commit()
    logout_user()
    return redirect(url_for('main.home'))
