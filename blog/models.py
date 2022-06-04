
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin

from blog import db, bcrypt, login_manager


# находим user_id и передать в login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='user'
    
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(1020), unique=True, nullable=False) 
    password = db.Column(db.String(60), nullable=False) 


    def set_password(self, password, hashed_password):
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.password})'
        
        