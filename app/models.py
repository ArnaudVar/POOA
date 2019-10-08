from app import db
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    series = db.Column(db.Text())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def list_serie(self):
        # Le format du texte est sous la forme {idserie}x{num_episode}-{idserie}x{num_episode} ...
        serie_episode_list = self.series.split('-')
        serie_list = []
        for serie_episode in serie_episode_list:
            serie_list.append(serie_episode.split('x'))
        return serie_list

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

