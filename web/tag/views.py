from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import TagForm
from web.db import session
from web.tag.models import Tag


blueprint = Blueprint('tag', __name__, url_prefix='/tag')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def tag_list():
    id = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    tag = session.query(Tag).filter(Tag.id == id and Tag.id_user == id_user).one_or_none()

    if not tag:
        tag = Tag()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(tag)
        session.commit()
        flash(f"Tag was deleted (id='{tag.id}', name='{tag.name}')")
        return redirect(url_for('tag.tag_list'))

    form = TagForm(obj=tag)

    if form.validate_on_submit():
        tag.add_form_data(form)
        session.add(tag)
        session.commit()
        if id:
            flash(f"Tag was updated (id='{tag.id}', name='{tag.name}')")
        else:
            flash(f"Tag was created (id='{tag.id}', name='{tag.name}')")
        return redirect(url_for('tag.tag_list'))

    to_form = {
        "title": "Tags",
        "id": id,
        "form": form,
        "tags": session.query(Tag).filter(Tag.id_user == id_user).order_by('id').all(),
    }
    return render_template("tag/list.html", **to_form)
