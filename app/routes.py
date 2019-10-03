from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', genres = ['Action','Aventure','Fiction','Pute'])


@app.route('/serie/<id>')
def serie(id):
    return render_template('serie.html', added=True, title="LE BLANKO", saisons=range(1,5), episodes=range(1,11), activeseason=1, activeepisode=1)
