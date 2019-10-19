from flask import render_template, Blueprint
from flask_login import login_required

blueprint = Blueprint('shared', __name__, url_prefix='/shared')


@blueprint.route('/')
@login_required
def shared_ops():
    return render_template("shared/list.html")
