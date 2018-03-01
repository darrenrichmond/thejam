from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProfileForm, CreateEditEventForm
import jamevents
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Event, Venue
from werkzeug.urls import url_parse

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = current_user
    #get the list of all open mic events in San Antonio. for now this is using test data with just Pigpen and Bob's
    events = jamevents.getEvents(user)
    print('Events in routes: ')
    print(events)
    print('****************')
    return render_template('index.html', appname='The Jam', app_page='Home', user=user, events=events)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', appname='The Jam', app_page='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', appname='The Jam', app_page='Register', form=form)

@app.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
    form = ProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        user.home_address = form.address.data
        db.session.add(user)
        db.session.commit()
        flash('Home address updated.')
        return redirect(url_for('index'))
    return render_template('user.html', appname='The Jam', app_page='Profile', form=form)

@app.route('/create', methods=['GET','POST'])
@login_required
def create_event():
    form = CreateEditEventForm()
    if form.validate():
        print("valid")
    print(form.errors)
    if form.validate_on_submit():
        print('Create Event Form Submitted')
        venue_name = form.venue_name.data
        venue_address = form.venue_address.data
        venue_website = form.venue_website.data
        venue = Venue(name=venue_name, address=venue_address, website=venue_website)
        db.session.add(venue)
        db.session.commit()
        event_night = form.event_night.data
        event_recurs = form.event_recurs.data
        event_start = form.event_start.data
        event_end = form.event_end.data
        adv_signup = form.event_adv_signup.data
        event_notes = form.event_notes.data
        venue_id = venue.id
        event = Event(night=event_night, recurs=event_recurs, start_time=event_start, end_time=event_end, adv_signup=adv_signup, notes=event_notes, venue_id=venue_id)
        db.session.add(event)
        db.session.commit()
        flash('Event created')
        return redirect(url_for('index'))
    return render_template('new_event.html', appname='The Jam', app_page='Create Event', form=form)

@app.route('/edit_event/<event_id>', methods=['GET','POST'])
@login_required
def edit_event(event_id):
    form = CreateEditEventForm()
    if form.validate():
        print("valid")
    print(form.errors)
    event = Event.query.get(event_id)
    venue = None
    if event:
        venue_id = event.venue_id
        venue = Venue.query.get(venue_id)
    else:
        flash('Could not find that event.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        venue.address = form.venue_address.data
        venue.website = form.venue_website.data
        db.session.add(venue)
        db.session.commit()
        event.night = form.event_night.data
        event.recurs = form.event_recurs.data
        event.start_time = form.event_start.data
        event.end_time = form.event_end.data
        event.adv_signup = form.event_adv_signup.data
        event.notes = form.event_notes.data
        db.session.add(event)
        db.session.commit()
        flash('Event updated!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
            form.venue_name.data = venue.name
            form.venue_address.data = venue.address
            form.venue_website.data = venue.website
            form.event_night.data = event.night
            form.event_recurs.data = event.recurs
            form.event_start.data = event.start_time
            form.event_end.data = event.end_time
            form.event_adv_signup.data = event.adv_signup
            form.event_notes.data = event.notes
    return render_template('edit_event.html', appname='The Jam', app_page='Create Event', form=form)