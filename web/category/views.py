from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import CategoryForm
from web.db import session
from web.category.models import Category
from web.tree import Tree


blueprint = Blueprint('category', __name__, url_prefix='/category')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def categories_list():
    id = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    category = session.query(Category).filter(Category.id == id and Category.id_user == id_user).one_or_none()

    if not category:
        category = Category()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(category)
        session.commit()
        flash(f"Category was deleted (id='{category.id}', name='{category.name}')")
        return redirect(url_for('category.categories_list'))

    form = CategoryForm(obj=category)
    categories = session.query(Category).filter(Category.id_user == id_user).order_by('id').all()
    tree = Tree(categories)
    form.parent_id.choices = tree.return_choises()

    if form.validate_on_submit():
        if form.parent_id.data == "0":
            form.parent_id.data = None
        category.add_form_data(form)
        session.add(category)
        session.commit()
        if id:
            flash(f"Category was updated (id='{category.id}', name='{category.name}')")
        else:
            flash(f"Category was created (id='{category.id}', name='{category.name}')")
        return redirect(url_for('category.categories_list'))

    to_form = {
        "title": "Categories",
        "id": id,
        "form": form,
        "categories": categories,
    }
    return render_template("category/list.html", **to_form)
