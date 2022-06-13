from datetime import datetime

from xmlrpc.client import DateTime
from flask_login import UserMixin
from blog import db, login_manager



# находим user_id и передать в login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Описание модели  User

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(1020), unique=True, nullable=False) 
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg') 
    password = db.Column(db.String(60), nullable=False) 
    last_seen = db.Column(db.DateTime)
    post = db.relationship('Post', backref='author', lazy=True)   # отношение между таблицей юзер и постом
    
    
    def __repr__(self):
        return f'User({self.id},{self.username}, {self.email}, {self.password})'
    
    
class Post(db.Model):
    __tablename__='posts'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(60), nullable=False)
    image_post = db.Column(db.String(30), nullable=True, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'User({self.title},{self.date_pasted}, {self.image_post})'
        
    