from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProfileForm
import jamevents
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = current_user
    #get the list of all open mic events in San Antonio. for now this is using test data with just Pigpen and Bob's
    events = jamevents.getEvents(user)
    

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