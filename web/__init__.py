from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from cfg import DB_STRING, SECRET_KEY

app = Flask(__name__)
app.config.from_object('cfg')

login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)

app.config['SECRET_KEY'] = SECRET_KEY
from web import views