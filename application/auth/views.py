from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm


@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/registerform.html", form = form)

    u = User(form.name.data, form.username.data, form.password.data, form.email.data)

    db.session().add(u)
    db.session().commit()
    
    # TODO: viesti muuten kuin errorin kautta?
    return render_template("auth/loginform.html", form = LoginForm(), error = "Account created successfully.")


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    
    if not form.validate():
        return render_template("auth/loginform.html", form = form)

    user = User.query.filter_by(username=form.username.data).first()
    
    if not user or not user.is_correct_password(form.password.data):
        return render_template("auth/loginform.html", form = form, error = "No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/account/", methods = ["GET", "POST"])
@login_required(role="ANY")
def my_account():
    if request.method == "GET":
        return render_template("auth/account.html", user = current_user)


@app.route("/auth/list/", methods = ["GET"])
@login_required(role="ADMIN")
def list_users():
    if request.method == "GET":
        return render_template("auth/list_users.html", users = User.query.all())

