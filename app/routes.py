from flask import render_template, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Sign In')

@app.route('/serie')
def serie():
    return render_template('serie.html', title='Serie')
