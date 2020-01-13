# noinspection DuplicatedCode
import time
from app import db

class Api:

    '''
    Classe statique utilisée pour communiquer avec l'api de The Movie Database.
    Chaque requête envers l'api se fait grâce à cette classe
    '''
    api_key = "4166d77f434aadc0fe7e430ab824f602"
    base_url_start = "https://api.themoviedb.org/3/"
    base_url_end = f"?api_key={api_key}&language=en-US"
    remaining_call = -1
    reset = int(time.time())

    @staticmethod
    def requete(url):
        '''
        Méthode utilisée pour effectuer une requete GET
        Une vérification de la réponse est réalisé.
        Si la réponse n'est correcte, cette méthode s'auto appelle
        :param url: string. L'url de la requête a effectuer
        :return: Le resultat de la requete en format json
        '''
        request = requests.get(url)
        if request.status_code == 200:
            Api.update_remaining(request)
            return request.json()
        elif request.status_code != 429:
            return request.json()
        else:
            time.sleep(1)
            return Api.requete(url)

    @staticmethod
    def check_api():
        '''
        Méthode utilisée pour vérifier combien de requête à l'Api il reste.
        Il peut y avoir 40 requetes toutes les 10 secondes.
        Dans le cas où il n'y a plus de requête disponible, cette méthode attend jusqu'au retour d'une requête
        :return: None
        '''
        now = int(time.time())
        if Api.remaining_call > 1 :
            return None
        else:
            temps = Api.reset - now
            time.sleep(abs(temps))
            return None

    @staticmethod
    def update_remaining(request):
        '''Méthode qui regarde combien de requêtes disponibles il reste et met a jour la variable "remaining_call"
        :return None'''
        now = int(time.time())
        headers = request.headers
        Api.remaining_call = int(headers['X-RateLimit-Remaining'])
        if now > Api.reset:
            Api.reset = now + 10
        return None


    @staticmethod
    def get_media(type_media, id_media):
        '''
        Méthode qui donne un média en fonction de son id
        :param type_media: string. Type du média recherché : 'tv' ou 'movie'
        :param id_media: int. Id du média
        :return: Un objet correspondant au média demandé
        '''
        Api.check_api()
        url = f"{Api.base_url_start}{type_media}/{id_media}{Api.base_url_end}"
        r = Api.requete(url)
        if type_media == 'movie':
            try:
                genre_list = []
                for x in r['genres']:
                    genre_list.append(x['name'])
                return Movie(id=r['id'], name=r['title'], description=r['overview'], grade=r['vote_average'],
                             image=r['poster_path'], genre=genre_list, date=r['release_date'])
            except:
                movie = None
                return movie
        else:
            try:
                genre_list = []
                for x in r['genres']:
                    genre_list.append(x['name'])
                if r['next_episode_to_air']:
                    serie = Serie(r['id'], r['name'], r['overview'], r['vote_average'],
                                  genre_list, r['poster_path'], {}, len(r['seasons']),
                                  r['last_episode_to_air'], r['next_episode_to_air']['air_date'])
                else:
                    serie = Serie(r['id'], r['name'], r['overview'], r['vote_average'],
                                  genre_list, r['poster_path'], {}, len(r['seasons']),
                                  r['last_episode_to_air'], '')
                for season in r['seasons']:
                    serie.seasons[season['season_number']] = season['episode_count']
            except:
                serie = None
            return serie

    """
    Cette methode permet d'obtenir les films ou les series populaires du moment a partir de l'API themoviedb
    """
    @staticmethod
    def get_popular(media, page, nb_page=0):
        '''
        Méthode qui donne la liste des médias populaire
        :param media: string. Type du média : 'tv' ou 'movie'
        :param page: int: Numéro de la page demandée
        :param nb_page: int. Nombre de page maximum
        :return: Un dictionnaire des médias les plus populaires
        '''
        Api.check_api()
        if media=='serie':
            url = f"{Api.base_url_start}tv/popular{Api.base_url_end}&sort_by=popularity.desc&page={page}"
        elif media=='movie':
            url = f"{Api.base_url_start}movie/popular{Api.base_url_end}&sort_by=popularity.desc&page={page}"
        result = Api.requete(url)
        if nb_page:
            return result['results'], result['total_pages']
        else:
            return result['results']


    """
    Cette methode permet d'obtenir les resultats d'une recherche sur le chaine "string" a la fois en films et en series
    """
    @staticmethod
    def search(string, page):
        Api.check_api()
        base_url_tv = f"{Api.base_url_start}search/tv{Api.base_url_end}&query={string}&page={page}&"\
                      "sort_by=popularity.desc"
        base_url_movies = f"{Api.base_url_start}search/movie{Api.base_url_end}&query={string}&page={page}&"\
                          "sort_by=popularity.desc"
        Api.check_api()
        search_serie = Api.requete(base_url_tv)
        Api.check_api()
        search_movie = Api.requete(base_url_movies)
        list_series = search_serie['results']
        list_movies = search_movie['results']
        nb_pages = max(int(search_serie['total_pages']), int(search_movie['total_pages']))
        return list_series, list_movies, nb_pages


    """
    Cette methode permet d'avoir les genres associes a un film ou une serie
    """
    @staticmethod
    def get_genre(media):
        Api.check_api()
        url = f"{Api.base_url_start}genre/{media}/list{Api.base_url_end}"
        request = Api.requete(url)
        media_genre = request['genres']
        return media_genre

    """
    Cette methode permet d'obtenir les films ou les series associes au genre "genre"
    """
    @staticmethod
    def discover(media, id_genre, page):
        Api.check_api()
        url = f"{Api.base_url_start}discover/{media}{Api.base_url_end}" \
              f"&with_genres={id_genre}&sort_by=popularity.desc&page={page}"
        request = Api.requete(url)
        list_media = request['results']
        nb_pages = int(request['total_pages'])
        return list_media, nb_pages

    """
    Cette methode permet d'obtenir l'objet episode associe a l'ID de la serie "id_serie", au numero de la saison "season"
    et au numero de l'episode "episode_number"
    """
    @staticmethod
    def get_episode(id_serie, season, episode_number):
        Api.check_api()
        url = f"{Api.base_url_start}tv/{id_serie}/season/{season}/episode/{episode_number}{Api.base_url_end}"
        episode_json = Api.requete(url)
        episode_code = 'S' + str(episode_json['season_number']) + 'E' + str(episode_json['episode_number'])
        episode = Episode(id=episode_code, name=episode_json['name'], description=episode_json["overview"],
                          cast=episode_json["guest_stars"], grade=episode_json["vote_average"],
                          image=episode_json["still_path"], id_serie=id_serie, num_season=season,
                          num_episode=episode_number, release=episode_json["air_date"])
        return episode


    """
    Cette methode permet d'avoir les films ou les series similaires au film ou a la serie d'ID "id"
    """
    @staticmethod
    def get_similar(id,media_type):
        Api.check_api()
        url = f"{Api.base_url_start}{media_type}/{id}/similar{Api.base_url_end}"
        similar_json = Api.requete(url)
        try:
            results = similar_json["total_results"]
            media_list = []
            if results >= 12:
                for i in range(12):
                    media = similar_json["results"][i]
                    if media_type == "movie":
                        media_list.append(Movie(id=media['id'], name=media['title'], description=None,
                                                grade=None, image=media['poster_path'], genre=None,
                                                date=None))
                    if media_type == "tv":
                        media_list.append(Serie(id=media['id'], name=media['name'], description=None, grade=None,
                                          image=media['poster_path'], genre=None, seasons=None, seasons_count=None,
                                          latest=None, date=None))
            else:
                for i in range(results):
                    media = similar_json["results"][i]
                    if media_type == "movie":
                        media_list.append(Movie(id=media['id'], name=media['title'], description=None,
                                                grade=None, image=media['poster_path'], genre=None,
                                                date=None))
                    if media_type == "tv":
                        media_list.append(Serie(id=media['id'], name=media['name'], description=None, grade=None,
                                          image=media['poster_path'], genre=None, seasons=None, seasons_count=None,
                                          latest=None, date=None))
        except:
            media_list = []
        return media_list

    """
    Cette methode est appelee au moment du login de l'utilisateur pour lui donner un session ID necessaire
    a ce qu'il puisse noter un film ou une serie
    """
    @staticmethod
    def new_session():
        Api.check_api()
        url = f"{Api.base_url_start}authentication/guest_session/new?api_key={Api.api_key}"
        request = Api.requete(url)
        session = request['guest_session_id']
        return session

    """
    Cette methode permet d'envoyer une note a themoviedb pour le film ou la serie d'ID "id"
    """
    @staticmethod
    def rate(id, grade, media, session, user):
        Api.check_api()
        url = f"{Api.base_url_start}{media}/{id}/rating?api_key={Api.api_key}&guest_session_id={session}"
        params = {"value": int(grade)}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        request_passed = False
        while not request_passed:
            request = requests.post(url=url, params=params, headers=headers)
            if request.status_code == 401:
                new_session = Api.new_session()
                user.session_id = new_session
                db.session.commit()
                url = f"{Api.base_url_start}{media}/{id}/rating?api_key={Api.api_key}&guest_session_id={new_session}"
            if request.status_code == 201:
                Api.update_remaining(request)
                result = request.json()
                request_passed = True
        return result


    """
    Cette methode permet d'obtenir les films ou les series les mieux notes de la page "page"
    """
    @staticmethod
    def get_top_rated(media, page):
        Api.check_api()
        url = f"{Api.base_url_start}{media}/top_rated{Api.base_url_end}&sort_by=vote_average.desc&page={page}"
        result=Api.requete(url)
        return result['results'], result['total_pages']
        
import requests
from classes.movie import Movie
from classes.Serie import Serie
from classes.episode import Episode
