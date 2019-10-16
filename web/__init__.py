from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from .db import session, init_db, teardown_session

app = Flask(__name__)
app.config.from_object('cfg')
init_db(app)

login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)

from web import views


@app.teardown_appcontext
def cleanup(resp_or_exc):
    session.remove()
