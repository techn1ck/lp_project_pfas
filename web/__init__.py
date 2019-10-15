from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('cfg')

login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)

from web import views
