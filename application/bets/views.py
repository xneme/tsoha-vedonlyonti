from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.bets.models import Event, Bet, Comment, Participant
from application.bets.forms import EventForm, CommentForm, BetForm, ParticipantForm


@app.route("/bets/", methods=["GET"])
def list_events():
    return render_template("bets/list.html", open_events = Event.query.filter_by(approved = True), suggested_events = Event.query.filter_by(approved = False))


@app.route("/bets/newevent/", methods=["GET", "POST"])
@login_required(role="ANY")
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
    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm())


@app.route("/bets/<event_id>/comment/", methods=["POST"])
@login_required(role="ANY")
def comment(event_id):
    form = CommentForm(request.form)

    if not form.validate():
        return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = form, participants = Participant.query.all(), pform = ParticipantForm())

    c = Comment(form.text.data)
    c.like = form.like.data
    c.event_id = event_id
    c.account_id = current_user.id
    db.session().add(c)
    db.session().commit()

    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm())


@app.route("/bets/<event_id>/delete/", methods=["POST"])
@login_required(role="ADMIN")
def delete_event(event_id):

    db.session().delete(Comment.query.filter_by(event_id = event_id))
    db.session().delete(Event.query.get(event_id))
    db.session().commit()

    return redirect(url_for("list_events"))


@app.route("/bets/<event_id>/<comment_id>/delete/", methods=["POST"])
@login_required(role="ANY")
def delete_comment(event_id, comment_id):
    c = Comment.query.get(comment_id)

    if "ADMIN" in current_user.roles or c.account_id == current_user.id:
        db.session().delete(c)
        db.session().commit()
    
    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm())


@app.route("/bets/<event_id>/approve/", methods=["POST"])
@login_required(role="ADMIN")
def approve_event(event_id):

    event = Event.query.get(event_id)
    event.approved = True
    db.session().commit()
    
    return redirect(url_for("list_events"))


@app.route("/bets/add_participant/<event_id>", methods=["POST"])
@login_required(role="ANY")
def add_participant(event_id):
    form = ParticipantForm(request.form)

    if not form.validate():
        return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = form)

    p = Participant(form.name.data, form.description.data)
    db.session().add(p)
    db.session().commit()
    # TODO lisää myös eventtiin
    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm())


@app.route("/bets/<event_id>/bet/", methods=["POST"])
def bet(event_id):
    # TODO vedon asetus
    return render_template("bets/event.html", event = Event.query.get(event_id))

