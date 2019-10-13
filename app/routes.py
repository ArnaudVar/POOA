from flask import render_template, redirect, url_for, flash, request, g
import requests
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchForm
from app.mail import send_password_reset_email
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from classes.Serie import Serie
from datetime import datetime


api_key = "11893590e2d73c103c840153c0daa770"
tv_g = requests.get(f"http://api.themoviedb.org/3/genre/tv/list?api_key={api_key}&language=en-US")
tv_genres = tv_g.json()['genres']
movie_g = requests.get(f"http://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US")
movie_genres = movie_g.json()['genres']
logo_nom_source = "../static/assets/LogoNom.png"
logo_source = "../static/assets/Logo.png"

@app.route('/')
@app.route('/home')
@login_required
def home():
    r = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
    suggestions = r.json()['results']
    selection = []
    for i in range(12):
        selection.append(suggestions[i])
    return render_template('home.html', title='Home', suggestions=selection, nombre_series=12,
                           tv_genres=tv_genres, movie_genres=movie_genres)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, src = logo_source)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/serie/<id>')
@login_required
def serie(id):
    s = requests.get(
        "https://api.themoviedb.org/3/tv/" + str(id) + "?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
    seriejson = s.json()
    if seriejson['next_episode_to_air']:
        serie = Serie(seriejson['id'], seriejson['name'], seriejson['overview'], seriejson['vote_average'],
                      seriejson['genres'], seriejson['poster_path'], {}, len(seriejson['seasons']),
                      seriejson['last_episode_to_air'], seriejson['next_episode_to_air']['air_date'])
    else:
        serie = Serie(seriejson['id'], seriejson['name'], seriejson['overview'], seriejson['vote_average'],
                      seriejson['genres'], seriejson['poster_path'], {}, len(seriejson['seasons']),
                      seriejson['last_episode_to_air'], '')
        for season in seriejson['seasons']:
            serie.seasons[season['season_number']] = season['episode_count']
    return render_template('serie.html', serie=serie, user=current_user, tv_genres=tv_genres, movie_genres=movie_genres)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name = form.name.data, surname=form.surname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, src = logo_source)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('request_confirmed'))
        else:
            form.email.errors.append("No user has this email adress")
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form, src = logo_nom_source)


@app.route('/request_confirmed')
def request_confirmed():
    return render_template('request_confirmed.html', title='Request confirmed', src = logo_nom_source)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/add/<id>')
def add_serie(id):
    current_user.add_serie(id)
    return('',204)


@app.route('/remove/<id>')
def remove_serie(id):
    current_user.remove_serie(id)
    return('',204)


@app.route('/myseries/<user_id>')
@login_required
def myserie(user_id):
    base_url_start = "https://api.themoviedb.org/3/tv/"
    base_url_end = f"?api_key={api_key}&language=en-US"
    u = User.query.get(user_id)
    list_series = u.list_serie()
    list_serie_rendered = []
    nb_series = 0
    if list_series == "The user doesn't have any series":
        list_serie_rendered = list_series
    else:
        for tvshow in list_series:
            nb_series+=1
            r = requests.get(f"{base_url_start}{tvshow[0]}{base_url_end}").json()
            list_serie_rendered.append(Serie(r['id'],r['name'], r['overview'], r['vote_average'], r['genres'], r['poster_path'], {}, len(r['seasons']), r['last_episode_to_air'], ''))
    return render_template('mySeries.html', title='MySeries', list_series=list_serie_rendered, nb_series=nb_series,
                           tv_genres=tv_genres, movie_genres=movie_genres)


@app.route('/search2/<string>/<page>')
@login_required
def search2(string, page):
    base_url_tv = f"https://api.themoviedb.org/3/search/tv?query={string}&api_key={api_key}&" \
                  f"language=en-US&page={page}&sort_by=popularity.desc"
    base_url_movies = f"https://api.themoviedb.org/3/search/movie?query={string}&api_key={api_key}&" \
                      f"language=en-US&page={page}&sort_by=popularity.desc"
    r1 = requests.get(base_url_tv).json()
    r2 = requests.get(base_url_movies).json()
    list_series = r1['results']
    list_movies = r2['results']
    nb_pages = max(int(r1['total_pages']), int(r2['total_pages']))
    return render_template('search.html', title='Search', list_series=list_series, tv_genres=tv_genres, movie_genres=movie_genres,
                           list_movies=list_movies, nb_pages=nb_pages, current_page=int(page), search=string)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = 'en'


@app.route('/search')
@login_required
def search():
    return redirect(f'/search2/{g.search_form.s.data}/1')


@app.route('/genre/<media>/<genre>/<page>')
@login_required
def genre(media, genre, page):
    genres_url = f"https://api.themoviedb.org/3/genre/{media}/list?api_key={api_key}&language=en-US"
    genres_request = requests.get(genres_url).json()
    list_genres = genres_request['genres']
    id_genre = -1
    for i in range(len(list_genres)):
        if list_genres[i]['name'] == genre:
            id_genre = i
    id_genre = list_genres[id_genre]['id']
    url = f"http://api.themoviedb.org/3/discover/{media}?api_key={api_key}" \
          f"&with_genres={id_genre}&sort_by=popularity.desc&language=en-US&page={page}"
    request = requests.get(url).json()
    r = request['results']
    nb_pages = int(request['total_pages'])
    r = requests.get(url).json()['results']
    return render_template('genre.html', genre=genre, list_medias=r, media=media,
                           tv_genres=tv_genres, movie_genres=movie_genres, current_page=int(page), nb_pages = nb_pages)


@app.route('/serie/<id>/season/<season>/episode/<episode>')
def select_episode(id, season, episode):
    s = requests.get(
        "https://api.themoviedb.org/3/tv/" + str(id) + "?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
    seriejson = s.json()
    if seriejson['next_episode_to_air']:
        serie = Serie(seriejson['id'], seriejson['name'], seriejson['overview'], seriejson['vote_average'],
                      seriejson['genres'], seriejson['poster_path'], {}, len(seriejson['seasons']),
                      seriejson['last_episode_to_air'], seriejson['next_episode_to_air']['air_date'])
    else:
        serie = Serie(seriejson['id'], seriejson['name'], seriejson['overview'], seriejson['vote_average'],
                      seriejson['genres'], seriejson['poster_path'], {}, len(seriejson['seasons']),
                      seriejson['last_episode_to_air'], '')
    for seasonz in seriejson['seasons']:
        serie.seasons[seasonz['season_number']] = seasonz['episode_count']

    serie.selected_episode = 'S' + str(season) + 'E' + str(episode)
    return render_template('serie.html', serie=serie, user=current_user, tv_genres=tv_genres, movie_genres=movie_genres)