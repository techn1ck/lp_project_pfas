from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from cfg import Config

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)

from web import views
from .db import session

@app.teardown_appcontext
def cleanup(resp_or_exc):
    session.remove()
