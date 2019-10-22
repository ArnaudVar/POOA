from flask import render_template, redirect, url_for, flash, request, g
from app.api import Api
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchForm
from app.mail import send_password_reset_email
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from datetime import datetime

tv_genres = Api.get_genre('tv')
movie_genres = Api.get_genre('movie')
logo_nom_source = "../static/assets/LogoNom.png"
logo_source = "../static/assets/Logo.png"


@app.route('/')
@app.route('/home')
@login_required
def home():
    suggestions_serie, suggestions_movie = Api.get_popular()
    selection_serie, selection_movie = [], []
    for i in range(12):
        selection_serie.append(suggestions_serie[i])
        selection_movie.append(suggestions_movie[i])
    return render_template('home.html', title='Home', suggestions_serie=selection_serie,
                           suggestions_movie=selection_movie, nombre_series=12,
                           tv_genres=tv_genres, movie_genres=movie_genres)


@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info(msg='The user is logging in')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            app.logger.info(msg='Invalid Username !')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            app.logger.info(msg='Invalid Password !')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        app.logger.info(msg='Successful Login !')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, src=logo_source)


@app.route('/logout')
def logout():
    logout_user()
    app.logger.info(msg='Successful Logout !')
    return redirect(url_for('login'))


@app.route('/serie/<id>')
@login_required
def serie(id):
    serie = Api.get_serie(id)
    similar = Api.get_similar(id, 'tv')
    if serie is None:
        app.logger.info(msg=f'Incorrect Serie id')
        return render_template('404.html')
    else:
        if current_user.is_in_series(id):
            user_series = current_user.series.split('-')
            for user_serie in user_series:
                if user_serie.split('x')[0] == str(id):
                    serie.selected_episode = user_serie.split('x')[1]
        episode = serie.get_episode
        app.logger.info(msg=f'Successful query for the Serie id={serie.id} page')
        return render_template('serie.html', serie=serie, user=current_user,
                               tv_genres=tv_genres, movie_genres=movie_genres, similar=similar)


@app.route('/movie/<id>')
@login_required
def movie(id):
    movie = Api.get_movie(id)
    similar = Api.get_similar(id, 'movie')
    if movie is None:
        app.logger.info(msg=f'Incorrect Movie id')
        return render_template('404.html')
    else:
        app.logger.info(msg=f'Successful query for the Movie id={id} page')
        return render_template('movie.html', movie=movie, user=current_user, tv_genres=tv_genres,
                               movie_genres=movie_genres, similar=similar)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, surname=form.surname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        app.logger.info(msg='Successful registry')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, src=logo_source)


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
                           title='Reset Password', form=form, src=logo_nom_source)


@app.route('/request_confirmed')
def request_confirmed():
    return render_template('request_confirmed.html', title='Request confirmed', src=logo_nom_source)


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


@app.route('/add_serie/<id>')
@login_required
def add_serie(id):
    current_user.add_serie(id)
    app.logger.info(msg=f'Serie {id} successfully added')
    return serie(id)


@app.route('/remove_serie/<id>')
@login_required
def remove_serie(id):
    current_user.remove_serie(id)
    app.logger.info(msg=f'Serie {id} successfully removed')
    return serie(id)


@app.route('/add_movie/<id>')
@login_required
def add_movie(id):
    current_user.add_movie(id)
    app.logger.info(msg=f'Movie {id} successfully added')
    return (movie(id))


@app.route('/remove_movie/<id>')
@login_required
def remove_movie(id):
    current_user.remove_movie(id)
    app.logger.info(msg=f'Movie {id} successfully removed')
    return (movie(id))


@app.route('/myseries')
@login_required
def myserie():
    user_id = current_user.id
    u = User.query.get(user_id)
    list_series = u.list_serie()
    list_serie_rendered = []
    nb_series = 0
    if list_series == "The user doesn't have any series":
        list_serie_rendered = list_series
        app.logger.info(msg=f'MySeries page rendered without series')
    else:
        for tvshow in list_series:
            nb_series += 1
            serie = Api.get_serie(tvshow)
            list_serie_rendered.append(serie)
        app.logger.info(msg=f'MySeries page rendered')
        app.logger.info(msg=f'The series list has {nb_series} series')
    return render_template('mySeries.html', title='MySeries', list_series=list_serie_rendered, nb_series=nb_series,
                           tv_genres=tv_genres, movie_genres=movie_genres, user=current_user)


@app.route('/mymovies')
@login_required
def mymovies():
    user_id = current_user.id
    u = User.query.get(user_id)
    list_movies = u.list_movie()
    list_movies_rendered = []
    nb_movies = 0
    if list_movies == "The user doesn't have any movie":
        list_movies_rendered = list_movies
        app.logger.info(msg=f'MyMovies page rendered without movies')
    else:
        for movie in list_movies:
            nb_movies += 1
            m = Api.get_movie(movie)
            list_movies_rendered.append(m)
        app.logger.info(msg=f'MyMovies page rendered')
        app.logger.info(msg=f'The movies list has {nb_movies} movies')
    return render_template('myMovies.html', title='MyMovies', list_movies=list_movies_rendered, nb_movies=nb_movies,
                           tv_genres=tv_genres, movie_genres=movie_genres)


@app.route('/search2/<string>/<page>')
@login_required
def search2(string, page):
    list_series, list_movies, nb_pages = Api.search(string, page)
    app.logger.info(msg=f'Search page {page} rendered for : {string}')
    return render_template('search.html', title='Search', list_series=list_series, tv_genres=tv_genres,
                           movie_genres=movie_genres,
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
    if media == 'movie':
        list_genres = movie_genres
    elif media == 'tv':
        list_genres = tv_genres
    for i in range(len(list_genres)):
        if list_genres[i]['name'] == genre:
            index_genre = i
    id_genre = list_genres[index_genre]['id']
    list_media, nb_pages = Api.discover(media, id_genre, page)
    app.logger.info(msg=f'Genre request on : Genre = {genre}, Media = {media}, Page = {page}')
    return render_template('genre.html', genre=genre, list_medias=list_media, media=media,
                           tv_genres=tv_genres, movie_genres=movie_genres, current_page=int(page), nb_pages=nb_pages)


@app.route('/serie/<id>/season/<season>/episode/<episode>')
@login_required
def select_episode(id, season, episode):
    serie = Api.get_serie(id)
    similar = Api.get_similar(id, 'tv')
    serie.selected_episode = 'S' + str(season) + 'E' + str(episode)
    episode = serie.get_episode
    app.logger.info(msg=f'Selected Episode : Serie = {id}, Season = {season}, episode = {episode.num_episode}')
    return render_template('serie.html', serie=serie, user=current_user, episode=episode, similar=similar,
                           tv_genres=tv_genres, movie_genres=movie_genres)


@app.route('/serie/<id>/season/<season>/episode/<episode>/view')
@login_required
def next_episode(id, season, episode):
    string_episode = 'S' + str(season) + 'E' + str(episode)
    current_user.view_episode(string_episode, id)
    return (serie(id))


@app.route('/rate/<i>')
def rate(i):
    current_user.update_grade(float(2 * int(i)))
    return ('', 204)


@app.route('/serie/<id>/post/grade')
def post_series_grade(id):
    grade = current_user.current_grade
    current_user.grade(id, 'serie', grade)
    # requests.post("https://api.themoviedb.org/3/tv/" + str(id)+'/rating' + "?api_key=11893590e2d73c103c840153c0daa770&language=en-US", data = { "value" : grade})
    return serie(id)


@app.route('/movie/<id>/post/grade')
def post_movie_grade(id):
    grade = current_user.current_grade
    current_user.grade(id, 'movie', grade)
    # requests.post("https://api.themoviedb.org/3/tv/" + str(id)+'/rating' + "?api_key=11893590e2d73c103c840153c0daa770&language=en-US", data = { "value" : grade})
    return movie(id)


@app.route('/serie/<id>/unrate')
def unrate_serie(id):
    current_user.unrate('serie', id)
    return serie(id)


@app.route('/movie/<id>/unrate')
def unrate_movie(id):
    current_user.unrate('movie', id)
    return movie(id)
