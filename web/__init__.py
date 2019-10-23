from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from cfg.web_settings import Config
from .db import session


def create_app(config_obj):
    app = Flask(__name__)

    app.config.from_object(config_obj)
    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'user.login'
    Bootstrap(app)

    from web.user.models import User
    @login_manager.user_loader
    def load_user(id):
        return session.query(User).get(int(id))


def register_blueprints(app):
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


app = create_app(Config)
@app.teardown_appcontext
def cleanup(resp_or_exc):
    session.remove()
