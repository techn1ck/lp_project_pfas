from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from web.db import session
from web.tree import Tree
from web.account.models import Account
from web.category.models import Category
from web.operation.models import Operation
from web.tag.models import Tag


blueprint = Blueprint('shared', __name__, url_prefix='/shared')


@blueprint.route('/')
@login_required
def shared_ops():
    return render_template("shared/list.html")
