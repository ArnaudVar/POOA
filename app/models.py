from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time

from app.api import Api


class User(UserMixin, db.Model):
    """
    Classe User
    :param id: identifiant de l'utilisateur
    :param username: nom d'utilisateur
    :param email: email utilisateur
    :param name: prenom de l'utilisateur
    :param surname: nom de famille de l'utilisateur
    :param password_hash : mot de passe hash apres inscription de l'utilisateur
    :param current_grade: nombre correspondant a la note actuelle de l'utilisateur
    :param session_id: l'id_session donne par l'API MovieDB pour avoir une guest session pour l'utilisateur
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    current_grade = db.Column(db.Float)
    session_id = db.Column(db.String(64))
    user_media = db.relationship('UserMedia', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"Username : {self.username}, Name : {self.name}, Surname : {self.surname}, Email : {self.email}," \
               f" Series : {self.series}"


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def list_serie(self):
        """
        Cette methode permet de retourner la liste des id des series ajoutees par l'utilisateur
        Pour ce faire on effectue une jointure avec la table user_media
        :return: renvoie une liste de serie id
        """
        # We query the list of series of this user :
        # We only query the series and only the id of the series
        series = self.user_media.filter_by(media = 'serie').with_entities('media_id').all()
        serie_list = []

        for s in series:
            serie_list.append(s[0])
        return serie_list

    def list_movie(self):
        """
        Cette méthode est similaire à la méthode précedente, elle permet de retourner la liste des id des films
        ajoutés par l'utilisateur en utilisant la table user_media
        :return: list(int)
        """
        # We query the list of movies of this user :
        # We only query the series and only the id of the movies
        movies = self.user_media.filter_by(media='movie').with_entities('media_id').all()
        movie_list = []

        for m in movies:
            movie_list.append(m[0])
        return movie_list

    def is_in_series(self, id):
        """
        Cette methode permet de savoir si une serie est dans la liste des series de l'utilisateur
        On utilise la méthode list_serie
        :param id: int
        :return: boolean
        """
        # On s'assure que tous les changements ont été fait dans la base de données
        db.session.commit()

        # On récupère la liste des séries
        list_serie = self.list_serie()

        # On renvoie true si la liste des séries contient la série recherchée
        return int(id) in list_serie

    def has_movie(self,id):
        """
        Cette methode permet de savoir si un film est dans la liste des films de l'utilisateur
        On utilise la méthode list_movie
        :param id: int
        :return: boolean
        """
        # On s'assure que tous les changements ont été fait dans la base de données
        db.session.commit()

        # On récupère la liste des films
        list_movie = self.list_movie()

        # On renvoie true si la liste des films contient la film recherchée
        return int(id) in list_movie

    def add_serie(self, id_serie):
        """
        Cette methode permet d'ajoute une serie a l'utilisateur dans la table user_media
        Par defaut, la serie commence comme non a jour (nutd)
        :param id_serie: int
        :return: void
        """
        # On commence par verifier que la serie n'est pas deja dans la liste des series de l'utilisateur
        if not self.is_in_series(id_serie):
            # On ajoute la serie a l'utilisatur en la marquant comme nutd
            s = UserMedia(media='serie', media_id=int(id_serie),
                          season_id=1, episode_id=1, state_serie='nutd', user=self)
            # On inscrit les changements dans la base de donnees
            db.session.add(s)
            db.session.commit()

    def add_movie(self, id_movie):
        """
        Cette methode permet d'ajoute un film a l'utilisateur dans la table user_media
        Tous les champs spécifiques aux series sont laisses nulls
        :param id_movie: int
        :return: void
        """
        # On commence par verifier que le film n'est pas deja dans la liste des films de l'utilisateur
        if not self.has_movie(id_movie):
            # On ajoute le film a l'utilisateur en laissant les champs specifiques des series nulls
            m = UserMedia(media='movie', media_id=int(id_movie), user=self)
            # On inscrit les changements dans la base de donnees
            db.session.add(m)
            db.session.commit()

    def get_last_episode_viewed(self, id):
        """
        Cette methode permet de retourner le dernier episode vu pour la serie ayant l'id id
        :param id: int
        :return: string
        """
        # On effectue une requete sur la table user_media pour obtenir le dernier episode vu
        last_ep = self.user_media.filter_by(media='serie', media_id=id).with_entities('season_id', 'episode_id').all()

        # Si la serie n'est pas dans les series de l'utilisateur, on renvoie S1E1
        if not last_ep:
            return('S1E1')
        else:
            res = last_ep[0]
            return f"S{res[0]}E{res[1]}"

    def is_after(self, season, episode, serie):
        """
        Cette methode sert a determiner si un episode de la saison "season" et de numero d'episode "episode"
        est posterieur au dernier episode vu par l'utilisateur pour la serie qui a l'ID "serie"
        :param season: int
        :param episode: int
        :param serie: int
        :return: boolean
        """
        last_ep = self.user_media.filter_by(media='serie', media_id=int(serie))\
            .with_entities('season_id', 'episode_id').all()
        # Si l'utilisateur n'a pas vu la serie, la reponse est forcement vraie
        if not last_ep:
            return True
        else:
            s, e = last_ep[0]
            # Soit l'episode est dans une saison posterieure, soit l'episode est plus grand dans la meme saison
            return s < int(season) or (s == int(season) and e < int(episode))

    def view_episode(self, episode, season, serie):
        """
        Cette methode permet de remplacer le dernier episode vu par l'utilisateur pour la serie d'ID "serie"
        par l'episode "episode".
        On va donc remplacer le code de l'episode et de la saison dans UserMedia par les bons codes
        Cette methode met egalement le statut de la serie a jour (utd/fin/nutd)
        :param episode: string
        :param serie: int
        :return: void
        """
        show = self.user_media.filter_by(media='serie', media_id=int(serie)).first()

        # Si la serie n'est pas dans les series de l'utilisateur, on ne fait rien
        if show:
            # On appelle l'API pour obtenir les informations de la serie
            s = Api.get_serie(str(serie))

            # On recupere la saison et le numero du dernier episode sorti
            latest_season, latest_ep = s.latest['season_number'], s.latest['episode_number']

            status = ''
            # Si le dernier episode et lepisode vu par l'utilisateur sont les memes, on regarde si il y a un
            # episode qui doit sortir
            if int(latest_season) == int(season) and int(latest_ep) == int(episode):
                # Si il n'y a pas d'episode a venir, la serie est terminee
                if s.date == '':
                    # On change le statut de la serie a fin
                    status = 'fin'
                else:
                    # Sinon on change le statut de la serie a a jour (utd)
                    status = 'utd'
            else:
                # Sinon la serie n'est pas a jour car il reste des episodes a voir, on change le statut en nutd
                status = 'nutd'

            # On update la saison et l'episode de l'utilisateur
            show.season_id = season
            show.episode_id = episode
            show.state_serie = status

            db.session.commit()

    def remove_serie(self,id_serie):
        """
        Cette methode permet d'enlever une serie des series suivies par l'utilisateur (dans la table UserMedia)
        :param id_serie: int
        :return: void
        """
        # We delete the record from the UserMedia table
        show = self.user_media.filter_by(media='serie', media_id=int(id_serie)).first()

        # We delete the show only if it is in the user list
        if show:
            db.session.delete(show)
            db.session.commit()

    def remove_movie(self, id_movie):
        """
        Cette methode permet d'enlever un film des films suivis par l'utilisateur (dans la table UserMedia)
        :param id_movie: int
        :return: void
        """
        # We delete the record from the UserMedia table
        movie = self.user_media.filter_by(media='movie', media_id=int(id_movie)).first()

        # We delete the show only if it is in the user list
        if movie:
            db.session.delete(movie)
            db.session.commit()

    def update_grade(self, new_grade):
        """
        Cette methode permet de changer la note actuelle de l'utilisateur quand il clique sur une etoile
        :param new_grade: int
        :return: void
        """
        self.current_grade = int(new_grade)
        db.session.commit()

    def grade(self, id, type, grade):
        """
        Cette methde permet d'affecter une note a un film ou une serie dans la table UserMedia
        :param id: int
        :param type: string
        :param grade: int
        :return: void
        """
        # We query the correct media
        media = self.user_media.filter_by(media=type, media_id=int(id)).first()

        # If the media is in the user's medias, we update its grade
        if media:
            media.media_grade = int(grade)
            db.session.commit()

    def is_graded(self, type, id):
        """
        Cette methode permet de savoir si l'on a deja note une serie ou un film
        :param type: string
        :param id: int
        :return: boolean
        """
        # On recupere le bon media
        media = self.user_media.filter_by(media=type, media_id=int(id)).first()

        # Si le media n'est pas dans les series ou les films de l'utilisateur, on renvoie faux
        if not media:
            return False
        else:
            # Si le media n'est pas note on renvoie faux
            if not media.media_grade:
                return False
            else:
                return True

    def get_grade(self, type, id):
        """
        Cette methode permet d'obtenir la note donne par l'utilisateur a un film ou une serie
        :param type: string
        :param id: int
        :return: int
        """
        # On recupere le bon media
        media = self.user_media.filter_by(media=type, media_id=int(id)).first()

        # Si le media est bien dans les medias de l'utilisateur
        if media:
            if not media.media_grade:
                return False
            else:
                return media.media_grade
        else:
            return False

    def unrate(self, type, id):
        """
        Cette methode permet de retirer la note associee a un media pour l'utilisateur
        :param type: string
        :param id: int
        :return: void
        """
        # On recupere le bon media
        media = self.user_media.filter_by(media=type, media_id=int(id)).first()

        # On regarde si le media est dans la liste de l'utilisateur
        if media and media.media_grade is not None:
            media.media_grade = None
            db.session.commit()

    """
    Ces methodes sont utilisees lorsque l'utilisateur souhaite reinitialiser sont mot de passe
    """
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def update_all_upcoming_episodes(self):
        """
        Cette methode est appelee lorsque l'user se connecte sur le site
        Avec cette methode, on met a jour les statuts de tous les series de l'utilisateur
        Pour ce faire, on parcourt la liste des series de l'utilisateur et on compare le dernier episode vu par
            l'utilisateur avec le dernier episode de la serie selon l'API. Si l'utilisateur est au dernier, on
            regarde si l'API contient un episode futur
        On ne lance cette methode qu'a chaque connexions de l'utilisateur afin de ne pas trop appeler l'API
        :return: void
        """
        # On recupere toutes les series de l'utilisateur
        serie = self.user_media.filter_by(media='serie').all()

        for s in serie:
            # On recupere les infos de chaque serie grace a l'API
            serie_info = Api.get_serie(s.media_id)

            # On recupere les infos de l'API sur le dernier episode
            last_season, last_ep = serie_info.latest['season_number'], serie_info.latest['episode_number']

            status = ''
            # Si le dernier episode vu par l'utilisateur est le dernier episode selon l'API, on regarde si il y a un
            # episode attendu pour savoir si l'utilisateur est a la fin de la serie
            if int(s.season_id) == last_season and int(s.episode_id) == last_ep:
                if serie_info.date == '':
                    # On met a jour le statut de la serie en finie (fin)
                    status = 'fin'
                else :
                    status = 'utd'
            else:
                status = 'nutd'

            # On met a jour le statut dans la BDD
            s.state_serie = status
        db.session.commit()

    def check_upcoming_episodes(self):
        """
        Cette methode est pour obtenir sur quelles series l'utilisateur est a jour, ne l'est pas ou a fini
        On retourne
        - La liste des series ou l'utilisateur est a jour
        - La liste des series ou l'utilisateur n'est pas a jour
        - La liste des seriesque l'utilisateur a fini
        :return: tuple de 3 listes
        """
        # On recupere toutes les series
        list_serie = self.user_media.filter_by(media='serie').all()

        list_series_up_to_date = []
        list_series_not_up_to_date = []
        list_series_finished = []

        # On parcourt nos series en regardant leur statut
        for serie in list_serie:
            if serie.state_serie == 'fin':
                list_series_finished.append(serie.media_id)
            elif serie.state_serie == 'utd':
                list_series_up_to_date.append(serie.media_id)
            else:
                list_series_not_up_to_date.append(serie.media_id)
        return list_series_up_to_date, list_series_not_up_to_date, list_series_finished

    def get_notifications(self):
        """
        Cette methode renvoie une liste contenant le nom des series et leur id
        :return: tuple list
        """
        # On recupere la liste des series ou l'utilisateur n'est pas jour
        list_series = self.check_upcoming_episodes()[1]
        notifs = []
        for serie in list_series:
            # On recupere les infos de chaque serie non a jour avec l'API
            serieobj = Api.get_serie(int(serie))
            notifs.append((serieobj.name, int(serie)))
        return notifs

    def nb_not_up_to_date(self):
        """
        Cette methode renvoie le nombre de series non a jour (pour pouvoir creer l'icone de notifications)
        :return: int
        """
        return len(self.check_upcoming_episodes()[1])


class UserMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Can be movie or serie
    media = db.Column(db.String)

    # The media id
    media_id = db.Column(db.Integer)

    # The season number (null if the media is a movie)
    season_id = db.Column(db.Integer)

    # The episode number (null if the media is a movie)
    episode_id = db.Column(db.Integer)

    # The state of the serie (null if the medai is a movie)
    # This column is used for notifying the users
    state_serie = db.Column(db.String)

    # la note accordee par l'utilisateur au media
    media_grade = db.Column(db.Integer)


    def __repr__(self):
        """
        Method used to return the information of a given user/media couple
        :return: void
        """
        user = User.query.get(int(self.user_id))
        if self.media == "movie":
            return f"The user {self.user_id} ({user.name} {user.surname}) has watched the movie {self.media_id}"
        else :
            return f"User : {self.user_id} ({user.name} {user.surname}) has watched the serie {self.media_id} " \
                   f"and the last episode he viewed is S{self.season_id}xE{self.episode_id}"


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

