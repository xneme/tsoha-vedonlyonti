from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.bets.models import Event, Bet, Comment
from application.bets.forms import EventForm, CommentForm, BetForm


@app.route("/bets/", methods=["GET"])
def list_events():
    return render_template("bets/list.html", open_events = Event.query.all(), suggested_events = Event.query.all())


@app.route("/bets/newevent/", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "GET":
        return render_template("bets/newevent.html", form = EventForm())

    form = EventForm(request.form)

    if not form.validate():
        return render_template("bets/newevent.html", form = form)

    e = Event(form.name.data, form.description.data, current_user.id)
    e.approved = False
    db.session().add(e)
    db.session().commit()
    # TODO toimiiko current_user.id?
    return redirect(url_for("list_events"))


@app.route("/bets/<event_id>/", methods=["GET"])
def show_contest(event_id):
    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.all(), form = CommentForm())


@app.route("/bets/<event_id>/", methods=["POST"])
@login_required
def comment(event_id):
    form = CommentForm(request.form)

    if not form.validate():
        return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.all(), form = form)

    c = Comment(form.text.data)
    c.like = form.like.data
    c.event_id = event_id
    c.account_id = current_user.id
    db.session().add(c)
    db.session().commit()

    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.all(), form = CommentForm())


@app.route("/bets/<event_id>/delete/", methods=["POST"])
@login_required
def delete_event(event_id):

    db.session().delete(Event.query.get(event_id))
    db.session().commit()

    return redirect(url_for("list_events"))


@app.route("/bets/<event_id>/bet/", methods=["POST"])
def bet(event_id):
    # TODO vedon asetus
    return render_template("bets/event.html", event = Event.query.get(event_id))

