from flask import Flask, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from web.models import create_engine
from cfg import DB_STRING, SECRET_KEY

# engine = create_engine(DB_STRING)
app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)

app.config['SECRET_KEY'] = SECRET_KEY
from web import views