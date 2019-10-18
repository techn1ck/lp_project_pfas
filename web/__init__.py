from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


from cfg import Config


app = Flask(__name__)
app.config.from_object(Config)


from web.account.views import blueprint as account_blueprint
from web.category.views import blueprint as category_blueprint
from web.operation.views import blueprint as operation_blueprint
from web.report.views import blueprint as report_blueprint
from web.shared.views import blueprint as shared_blueprint
from web.tag.views import blueprint as tag_blueprint
from web.user.views import blueprint as user_blueprint

app.register_blueprint(account_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(operation_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(shared_blueprint)
app.register_blueprint(tag_blueprint)
app.register_blueprint(user_blueprint)

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
Bootstrap(app)


from .db import session
from web.user.models import User


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))


"""
@app.teardown_appcontext
def cleanup(resp_or_exc):
    session.remove()
"""