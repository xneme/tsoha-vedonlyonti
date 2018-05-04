from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.bets.models import Event, Bet, Comment, Participant
from application.bets.forms import EventForm, CommentForm, BetForm, ParticipantForm, EventParticipantForm


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
    e.date_start = form.date_start.data
    e.date_end = form.date_end.data
    db.session().add(e)
    db.session().commit()
    # TODO toimiiko current_user.id?
    return redirect(url_for("list_events"))


@app.route("/bets/<event_id>/", methods=["GET"])
def show_contest(event_id):
    epform = EventParticipantForm()
    epform.participant_id.choices = [(p.id, p.name) for p in Participant.query.order_by('name')]
    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Event.query.get(event_id).participants, pform = ParticipantForm(), epform = epform)


@app.route("/bets/<event_id>/participants/", methods=["GET", "POST"])
@login_required(role="ANY")
def event_participants(event_id):
    if request.method == "GET":
        epform = EventParticipantForm()
        epform.participant_id.choices = [(p.id, p.name) for p in Participant.query.order_by('name')]
        return render_template("bets/eventparticipants.html", event = Event.query.get(event_id), participants = Event.query.get(event_id).participants, pform = ParticipantForm(), epform = epform)


@app.route("/bets/<event_id>/comment/", methods=["POST"])
@login_required(role="ANY")
def comment(event_id):
    form = CommentForm(request.form)
    epform = EventParticipantForm()
    epform.participant_id.choices = [(p.id, p.name) for p in Participant.query.order_by('name')]

    if not form.validate():
        return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = form, participants = Participant.query.all(), pform = ParticipantForm(), epform = epform)

    c = Comment(form.text.data)
    c.like = form.like.data
    c.event_id = event_id
    c.account_id = current_user.id
    db.session().add(c)
    db.session().commit()

    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm(), epform = epform)


@app.route("/bets/<event_id>/delete/", methods=["POST"])
@login_required(role="ADMIN")
def delete_event(event_id):

#    db.session().delete(Comment.query.filter_by(event_id = event_id))
    db.session().delete(Event.query.get(event_id))
    db.session().commit()

    return redirect(url_for("list_events"))


@app.route("/bets/<event_id>/<comment_id>/delete/", methods=["POST"])
@login_required(role="ANY")
def delete_comment(event_id, comment_id):
    c = Comment.query.get(comment_id)
    epform = EventParticipantForm()
    epform.participant_id.choices = [(p.id, p.name) for p in Participant.query.order_by('name')]

    if "ADMIN" in current_user.roles or c.account_id == current_user.id:
        db.session().delete(c)
        db.session().commit()
    
    return render_template("bets/event.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm(), epform = epform)


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
    epform = EventParticipantForm()
    epform.participant_id.choices = [(p.id, p.name) for p in Participant.query.order_by('name')]

    if not form.validate():
        return render_template("bets/eventparticipants.html", event = Event.query.get(event_id), participants = Event.query.get(event_id).participants, pform = form, epform = epform)

    p = Participant(form.name.data, form.description.data)
    e = Event.query.get(event_id)
    e.participants.append(p)
    db.session().add(e)
    db.session().commit()
    return render_template("bets/eventparticipants.html", event = Event.query.get(event_id), participants = Event.query.get(event_id).participants, pform = ParticipantForm(), epform = epform)


@app.route("/bets/add_eventparticipant/<event_id>", methods=["POST"])
@login_required(role="ANY")
def add_eventparticipant(event_id):
    form = EventParticipantForm(request.form)
    print("saatiin :" + str(form.participant_id.data))
    e = Event.query.get(event_id)
    p = Participant.query.get(form.participant_id.data)
    e.participants.append(p)
    db.session().add(e)
    db.session().commit()
    # TODO lisää myös eventtiin
    epform = EventParticipantForm()
    epform.participant_id.choices = [(p.id, p.name) for p in Participant.query.order_by('name')]
    return render_template("bets/eventparticipant.html", event = Event.query.get(event_id), comments = Comment.query.filter_by(event_id = event_id), form = CommentForm(), participants = Participant.query.all(), pform = ParticipantForm(), epform = epform)


@app.route("/bets/<event_id>/bet/", methods=["GET", "POST"])
@login_required(role="ANY")
def bet(event_id):
    bform = BetForm()
    bform.participant.choices = [(p.id, p.name) for p in Event.query.get(event_id).participants]
    if request.method == "GET":
        return render_template("bets/eventbet.html", event = Event.query.get(event_id), form = bform)
    # TODO vedon asetus
    
    form = BetForm(request.form)
    b = Bet(form.amount.data, current_user.id, event_id, form.participant.data)
    db.session().add(b)
    db.session().commit()
    return render_template("bets/eventbet.html", event = Event.query.get(event_id), form = bform)

