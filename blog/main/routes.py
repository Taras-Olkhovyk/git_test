
from crypt import methods
from flask import render_template, flash, redirect, request, url_for, Blueprint
from blog.main.forms import LoginForm
from blog.models import User
from blog.models import check_password_hash
from flask_login import login_user, current_user, login_required

main=Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='Главня')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # забераем данные по емейлу у первого попавшего пользователя
        user = User.query.filter_by(email=form.email.data).first() 
        # если пользователь и пароль совпадают то пользователь логинится 
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            flash('Войти не удалось. Пожалуста, проверте електронную почту и пароль', 'danger')
    return render_template('login.html', title='Авторизация', form=form)

@main.route('/account')
@login_required
def account():
    return render_template('account.html', title='Акаунт', current_user=current_user)

@main.route('/logout')
def logout():
    return redirect(url_for('main.index'))