from flask import render_template, flash, redirect
from web import app
#from web.models import User, Account
from .forms import AccountForm

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/accounts/', methods = ['GET', 'POST'])
def accounts():
    form = AccountForm()
    if form.validate_on_submit():
        flash('name="' + form.name.data + '", description=' + form.description.data + '", currency=' + form.currency.data)
        return redirect('/index')

    return render_template("account_form.html", title = "Accounts", form=form)