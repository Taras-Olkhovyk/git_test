import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


SECRET_KEY=os.urandom(36)
SQLALCHEMY_DATEBASE_URI=os.environ.get('SQLALCHEMY_DATEBASE_URI')
SQLACHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLACHEMY_TRACK_MODIFICATIONS')