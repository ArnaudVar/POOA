from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time

from app.api import Api


class User(UserMixin, db.Model):
    """
    Classe User : une classe pour definir les utilisateurs de l'application

    Cette classe correspond au modele de la table user de la base de donnees.
    On y trouve donc tous les paramètres de la table :

    :param id: (int) identifiant de l'utilisateur
    :param username: (int) nom d'utilisateur
    :param email: (string) email utilisateur
    :param name: (string) prenom de l'utilisateur
    :param surname: (string) nom de famille de l'utilisateur
    :param password_hash : (string) mot de passe hash apres inscription de l'utilisateur
    :param current_grade: (string) nombre correspondant a la note actuelle de l'utilisateur
    :param session_id: (string) l'id_session donne par l'API MovieDB pour avoir une guest session pour l'utilisateur
    :param notifications: (binary) un binaire nous indiquant si les notifications ont ete vues par l'utilisateur
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    current_grade = db.Column(db.Float)
    session_id = db.Column(db.String(64))
    notifications = db.Column(db.Binary)
    user_media = db.relationship('UserMedia', backref='user', lazy='dynamic')

    def __init__(self, username, email, name, surname, password):
        """
        Constructeur de la classe User

        Prend 5 parametres en compte lors de la creation de l'utilisateur
        :param username: (String) username de l'utilisateur
        :param email: (String) email de l'utilisateur
        :param name: (String) name de l'utilisateur
        :param surname: (String) surname de l'utilisateur
        :param password: (String) password de l'utilisateur

        Le password est encode avec la fonction generate_password_hash pour que les mots de passes ne soient pas
        stockes en clair dans la base de donnees
        Le reste des donnes est initialise a null
        """
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        """
        Methode nous permettant de representer nos utilisateurs sous la forme de chaines de caracteres

        On retourne l'username, le nom, le prenom, l'email, les series et les films de l'utilisateur
        Pour ce faire on fait appel aux methodes list_serie et list_movie definies dans la classe User

        :return: String
        """
        return f"Username : {self.username}, Name : {self.name}, Surname : {self.surname}, Email : {self.email},\n" \
               f"Series : {self.list_media(media='tv')}, \n" \
               f"Movies : {self.list_media(media='movie')}"

    def set_password(self, password):
        """Methode nous permettant de mettre a jour le mot de passe d'un utilisateur"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Methode nous permettant de verifier si un mot de passe est celui de l'utilisateur

        Pour comparer le mot de passe donné avec le hash stocke dans la base de donnees,
        on utilise la methode check_password_hash du module werkzeug.security

        :return: Boolean
        """
        return check_password_hash(self.password_hash, password)

    def list_media(self, media):
        """
        Methode retournant la liste des id des medias ajoutees (favoris) par l'utilisateur.

        On effectue une jointure de la table user_media grace a la relation one-to-many entre User et user_media.
        En effet, les objets de la classe user ont un champ user_media que l'on utilise pour effectuer la jointure.

        :param media: (string) type du media voulu
        :return: int list
        """
        # On selectionne les identifiants de tous les medias de l'utilisateur etant du bon type
        # On obtient une liste de tuples de taille 1 contenant les id des medias voulus
        medias = self.user_media.filter_by(media=media).with_entities('media_id').all()

        # Liste stockant le resultat de la methode
        media_list = []

        # On parcourt cette liste de tuples pour obtenir une liste d'idenfiants
        for m in medias:
            media_list.append(m[0])
        return media_list

    def is_in_medias(self, id_media, type_media):
        """
        Methode permettant de savoir si un media est dans les medias ajoutes par l'utilisateur

        On fait appel a la methode list_medias qui nous renvoie la liste des
            identifiants des medias du type cherche par l'utilisateur
        On parcourt cette liste et on regarde si l'identifiant cherche est dans la liste

        :param id_media: (int) identifiant du media que l'on recherche
        :param type_media: (string) type du media cherche (serie ou movie)
        :return: boolean
        """
        # On s'assure que tous les changements ont été fait dans la base de données
        db.session.commit()

        # On récupère la liste des medias cherches de la base de donnees
        list_medias = self.list_media(type_media)

        # On renvoie true si la liste des series contient la serie recherchee
        return int(id_media) in list_medias

    def add_media(self, id_media, type_media):
        """
        Cette methode permet d'ajoute un media a l'utilisateur dans la table user_media

        Par defaut, si le media est une serie, elle commence comme non a jour (nutd)
        sinon, les champs specifiques a une serie sont laisses vides
        On met a jour les notifications de l'utilisateur
        :param id_media: int
        :return: void
        """
        # On commence par verifier que le media n'est pas deja dans la liste des medias de l'utilisateur
        if not self.is_in_medias(id_media=id_media, type_media=type_media):
            if type_media == 'tv':
                # On ajoute la serie a l'utilisatur en la marquant comme nutd et on remeta jour les notifications
                m = UserMedia(media='tv', media_id=int(id_media),
                    season_id=1, episode_id=1, state_serie='nutd', user=self)
                self.notifications = bytes(1)

            else:
                m = UserMedia(media='movie', media_id=int(id_media), user=self)

            # On inscrit les changements dans la base de donnees
            db.session.add(m)
            db.session.commit()

    def get_last_episode_viewed(self, id_serie):
        """
        Cette methode permet de retourner le dernier episode vu pour la serie ayant l'id id_serie

        L'episode est retourne sous la forme SnEm où n est le numero de la saison et m le numero de l'episode
        Si l'episode n'est pas dans les series de l'utilisateur, on renvoie S1E1

        :param id_serie: int
        :return: string
        """
        # On effectue une requete sur la table user_media
        # pour obtenir le dernier episode vu de l'utilisateur pour cette serie
        # last_ep est un tuple (numero_saison, numero_episode)
        last_ep = self.user_media.filter_by(media='tv', media_id=id_serie).\
            with_entities('season_id', 'episode_id').all()

        # Si la serie n'est pas dans les series de l'utilisateur, on renvoie S1E1
        # Sinon on recupere lenumero du dernier episode
        if not last_ep:
            return('S1E1')
        else:
            res = last_ep[0]
            return f"S{res[0]}E{res[1]}"

    def is_after(self, season, episode, serie):
        """
        Cette methode permet de comparer le dernier episode vu avec un episode de la serie

        On determine si un episode de la saison "season" et de numero d'episode "episode"
        est posterieur au dernier episode vu par l'utilisateur pour la serie qui a l'ID "serie"
        Elle renvoie vrai si c'est le cas, faux sinon

        :param season: (int) numero de la saison de l'episode a tester
        :param episode: (int) numero de l'episode a tester
        :param serie: (int) identifiant de la serie

        :return: boolean
        """
        # On recupere les informations du dernier episode de cette serie vu par l'utilisateur
        last_ep = self.user_media.filter_by(media='tv', media_id=int(serie))\
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
        Cette methode permet de modifier le dernier episode vu par un utilisateur


        On remplace le dernier episode vu par l'utilisateur pour la serie d'ID "serie"
        par l'episode "episode" de la saison "season".

        On va donc remplacer le code de l'episode et de la saison dans UserMedia par les bons codes
        Cette methode met egalement le statut de la serie a jour (utd/fin/nutd)

        :param episode: (int) numero de l'episode a marquer comme vu
        :param season: (int) numero de la saison de cet episode
        :param serie: (int) identifiant de la serie
        :return: void
        """
        # On recupere la serie des series de l'utilisateur
        show = self.user_media.filter_by(media='tv', media_id=int(serie)).first()

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

            # On met a jour les notifications
            self.notifications = bytes(1)

            db.session.commit()

    def remove_media(self, id_media, type_media):
        """
        Cette methode permet d'enlever un media des medias suivis par l'utilisateur (dans la table UserMedia)

        :param id_media: (int) identifiant du media
        :param type_media: (string) type du media (serie ou movie)
        :return: void
        """
        # We get the record from the UserMedia table
        show = self.user_media.filter_by(media=type_media, media_id=int(id_media)).first()

        # We delete the show only if it is in the user list
        if show:
            db.session.delete(show)
            db.session.commit()

    def update_grade(self, new_grade):
        """
        Cette methode permet de changer la note actuelle de l'utilisateur quand il clique sur une etoile

        La note actuelle est la note de la page sur laquelle est l'utilisateur,
        on la stocke donc dans la table User

        :param new_grade: (int) la note selectionnee par l'utilisateur
        :return: void
        """
        self.current_grade = int(new_grade)
        db.session.commit()

    def grade(self, id_media, media, grade):
        """
        Cette methde permet d'affecter une note a un film ou une serie dans la table UserMedia

        :param id_media: (int) identifiant du media
        :param media: (string) type du media
        :param grade: (int) grade du media
        :return: void
        """
        # On recupere le bon media
        m = self.user_media.filter_by(media=media, media_id=int(id_media)).first()

        # Si le media est dans les medias de l'utilisateur, on le note
        if m:
            m.media_grade = int(grade)
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
        serie = self.user_media.filter_by(media='tv').all()

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
        list_serie = self.user_media.filter_by(media='tv').all()

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

        Elle ne renvoie la liste que si l'utilisateur doit avoir
        des notifications, sinon elle renvoie une liste vide
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
        if self.notifications:
            return len(self.get_notifications())
        else:
            return 0


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

