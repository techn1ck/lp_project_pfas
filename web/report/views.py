from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from web.db import session
from web.tree import Tree
from web.account.models import Account
from web.category.models import Category
from web.operation.models import Operation
from web.tag.models import Tag


blueprint = Blueprint('report', __name__, url_prefix='/report')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def reports():
    user_id = current_user.get_id()
    categories = session.query(Category).filter(Category.id_user == user_id).order_by('id').all()
    tree = Tree(categories)

    to_form = {
        "categories" : tree.return_tree(),
    }
    return render_template("report/main_report.html", **to_form)
