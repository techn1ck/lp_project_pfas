from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import TagForm
from web.db import session
from web.obj_history.db_history import save_original_state, get_obj_history, get_deleted_objects
from web.tag.models import Tag


blueprint = Blueprint('tag', __name__, url_prefix='/tag')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def tag_list():
    id_tag = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    action = request.args.get('action', default='', type=str)
    tag = get_current_tag(id_tag, id_user)

    if action == 'delete' and tag.id:
        delete_tag(tag)
        return redirect(url_for('tag.tag_list'))

    if action == 'switch' and tag.id:
        change_tag_actual(tag)
        return redirect(url_for('tag.tag_list'))

    form = TagForm(obj=tag)
    if form.validate_on_submit():
        save_tag(tag, form, id_tag)
        return redirect(url_for('tag.tag_list'))

    to_form = {
        "title": "Tags",
        "id": id_tag,
        "form": form,
        "current_tag": tag,
        "tags": get_tags_list(id_user),
        "tag_history": get_obj_history('Tag', tag.id),
        "deleted_tags": get_deleted_objects('Tag'),
    }
    return render_template("tag/list.html", **to_form)


def get_current_tag(id_tag, id_user):
    tag = session.query(Tag).filter(Tag.id == id_tag and Tag.id_user == id_user).one_or_none()
    if not tag:
        tag = Tag()
    return tag


def delete_tag(tag):
    save_original_state('Tag', tag.id, 'delete', tag)
    session.delete(tag)
    session.commit()
    flash(f"Tag was deleted (id='{tag.id}', name='{tag.name}')")


def save_tag(tag, form, id_tag):
    if tag.id:
        save_original_state('Tag', tag.id, 'update', tag)
    tag.add_form_data(form)
    session.add(tag)
    session.commit()
    if id_tag:
        flash(f"Tag was updated (id='{tag.id}', name='{tag.name}')")
    else:
        flash(f"Tag was created (id='{tag.id}', name='{tag.name}')")


def change_tag_actual(tag):
    save_original_state('Tag', tag.id, 'invert_is_actual', tag)
    tag.invert_is_actual()
    session.add(tag)
    session.commit()
    flash(f"Tag was switched (id='{tag.id}', name='{tag.name}')")


def get_tags_list(id_user):
    return session.query(Tag).filter(Tag.id_user == id_user).order_by('id').all()
