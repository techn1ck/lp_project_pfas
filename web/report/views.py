from flask import render_template, Blueprint
from flask_login import current_user, login_required

from web.db import session
from web.tree import Tree
from web.category.models import Category


blueprint = Blueprint('report', __name__, url_prefix='/report')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def reports():
    user_id = current_user.get_id()
    categories = session.query(Category).filter(Category.id_user == user_id).order_by('id').all()
    tree = Tree(categories)

    to_form = {
        "categories": tree.return_tree(),
    }
    return render_template("report/main_report.html", **to_form)
