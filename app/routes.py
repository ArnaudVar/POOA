from flask import render_template, redirect, url_for, flash
import requests
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask import request
from flask_login import login_required
from werkzeug.urls import url_parse
from classes.Serie import Serie
from classes.season import Season


@app.route('/')
@app.route('/home')
#@login_required
def home():
    r = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
    g = requests.get("http://api.themoviedb.org/3/genre/tv/list?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
    genres = g.json()['genres']
    suggestions = r.json()['results']
    selection = []
    for i in range(12):
        selection.append(suggestions[i])
    return render_template('home.html', title='Home', suggestions=selection, nombre_series=12, genres=genres)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/serie/<id>')
@login_required
def serie(id):
    s = requests.get("https://api.themoviedb.org/3/tv/" + str(id) + "?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
    seriejson = s.json()
    serie = Serie(seriejson['id'],seriejson['name'],seriejson['overview'], [], seriejson['vote_average'], seriejson['poster_path'], [], seriejson['last_episode_to_air'], seriejson['next_episode_to_air']['air_date'])
    for i,seasonjson in enumerate(s['seasons']):
        season = Season(seasonjson['id'], i, [], -1.0, seasonjson['poster_path'])
        for j in range(seasonjson['episode_count']):
            episodejson = requests.get("https://api.themoviedb.org/3/tv/" + str(id)+"/season/" + str(i) +"/episode/"+ str(j) +"?api_key=11893590e2d73c103c840153c0daa770&language=en-US").json()
            episode = Episode()
            season.listEpisode.append(episode)
        serie.seasons.append(season)
    return render_template('serie.html', title='Serie', serie=serie, activeseason=1, activeepisode=1)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name = form.name.data, surname = form.surname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

