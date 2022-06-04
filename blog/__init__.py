from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # спросить где брать логин. сохраняет данные для фун. логин
login_manager.login_message_category = 'danger'

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile('main/settings.py')
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from blog.main.routes import main
    app.register_blueprint(main)

    return app

app_ctx = create_app()

def create_user():
    with app_ctx.app_context():
        from blog.models import User
       
        
        db.create_all()
        hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
        user = User(username = 'Mike', email = 'mike_admin@blog.com', password = hashed_password)
        db.session.add(user)
        db.session.commit()
        