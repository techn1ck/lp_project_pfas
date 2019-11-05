from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import CategoryForm
from web.db import session
from web.category.models import Category
from web.operation.models import Operation
from web.obj_history.db_history import save_original_state, get_obj_history, get_deleted_objects
from web.tree import Tree


blueprint = Blueprint('category', __name__, url_prefix='/category')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def categories_list():
    id_cat = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    action = request.args.get('action', default='', type=str)
    category = get_current_category(id_cat, id_user)

    if action == 'delete' and category.id:
        if not check_is_empty_category(category.id):
            flash(f"Unable to delete category, it has operations. Please, empty category first", category='error')
            return redirect(url_for('category.categories_list'))
        elif not check_has_no_child_category(category.id):
            flash(f"Unable to delete category, it has children. Please, delete children first", category='error')
            return redirect(url_for('category.categories_list'))
        else:
            delete_category(category)
            return redirect(url_for('category.categories_list'))

    if action == 'switch' and category.id:
        change_category_actual(category)
        return redirect(url_for('category.categories_list'))

    form = CategoryForm(obj=category)
    categories = get_categories_list(id_user)
    tree = Tree(categories)
    form.parent_id.choices = tree.return_choises()

    if form.validate_on_submit():
        save_category(category, form, id_cat)
        return redirect(url_for('category.categories_list'))

    to_form = {
        "title": "Categories",
        "id": id_cat,
        "form": form,
        "current_category": category,
        "categories": categories,
        "category_history": get_obj_history('Category', category.id),
        "deleted_categories": get_deleted_objects('Category'),
    }
    return render_template("category/list.html", **to_form)


def get_current_category(id_cat, id_user):
    category = session.query(Category).filter(Category.id == id_cat and Category.id_user == id_user).one_or_none()
    if not category:
        category = Category()
    return category


def delete_category(category):
    save_original_state('Category', category.id, 'delete', category)
    session.delete(category)
    session.commit()
    flash(f"Category was deleted (id='{category.id}', name='{category.name}')")


def check_is_empty_category(id_cat):
    if not session.query(Operation).filter(Operation.id_cat == id_cat).first():
        return True


def check_has_no_child_category(id_cat):
    if not session.query(Category).filter(Category.parent_id == id_cat).first():
        return True


def save_category(category, form, id_cat):
    if category.id:
        save_original_state('Category', category.id, 'update', category)
    if not form.parent_id.data:
        form.parent_id.data = None
    print(form)
    category.add_form_data(form)
    session.add(category)
    session.commit()
    if id_cat:
        flash(f"Category was updated (id='{category.id}', name='{category.name}')")
    else:
        flash(f"Category was created (id='{category.id}', name='{category.name}')")


def change_category_actual(category):
    save_original_state('Category', category.id, 'invert_is_actual', category)
    category.invert_is_actual()
    session.add(category)
    session.commit()
    flash(f"Category was switched (id='{category.id}', name='{category.name}')")


def get_categories_list(id_user):
    return session.query(Category).filter(Category.id_user == id_user).order_by('id').all()
