# noinspection DuplicatedCode
class Api:

    api_key = "11893590e2d73c103c840153c0daa770"
    base_url_start = "https://api.themoviedb.org/3/"
    base_url_end = f"?api_key={api_key}&language=en-US"
    """
    Cette methode permet de creer un objet movie a partir de son ID et d'une requete a l'API themoviedb
    """
    @staticmethod
    def get_movie(id):
        r = requests.get(f"{Api.base_url_start}movie/{id}{Api.base_url_end}").json()
        try :
            genre_list = []
            for x in r['genres']:
                genre_list.append(x['name'])
            return Movie(id=r['id'], name=r['title'], description=r['overview'], grade=r['vote_average'],
                         image=r['poster_path'], genre=genre_list, date=r['release_date'])
        except :
            movie = None
            return movie

    """
    Cette methode permet de creer un objet serie a partir de son ID et d'une requete a l'API themoviedb
    """
    @staticmethod
    def get_serie(id):
        seriejson = requests.get(f"{Api.base_url_start}tv/{id}{Api.base_url_end}").json()
        try :
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
        except :
            serie = None
        return serie

    """
    Cette methode permet d'obtenir les films ou les series populaires du moment a partir de l'API themoviedb
    """
    @staticmethod
    def get_popular(media, page, nb_page=False):
        if media=='serie':
            result = requests.get(f"{Api.base_url_start}tv/popular{Api.base_url_end}&"
                                  f"sort_by=popularity.desc&page={page}").json()
        elif media=='movie':
            result = requests.get(f"{Api.base_url_start}movie/popular{Api.base_url_end}&"
                                  f"sort_by=popularity.desc&page={page}").json()
        else:
            raise ValueError("The type of this media is unknown")
        if nb_page:
            return result['results'], result['total_pages']
        else:
            return result['results']


    """
    Cette methode permet d'obtenir les resultats d'une recherche sur le chaine "string" a la fois en films et en series
    """
    @staticmethod
    def search(string, page):
        base_url_tv = f"{Api.base_url_start}search/tv{Api.base_url_end}&query={string}&page={page}&"\
                      "sort_by=popularity.desc"
        base_url_movies = f"{Api.base_url_start}search/movie{Api.base_url_end}&query={string}&page={page}&"\
                          "sort_by=popularity.desc"
        search_serie = requests.get(base_url_tv).json()
        search_movie = requests.get(base_url_movies).json()
        list_series = search_serie['results']
        list_movies = search_movie['results']
        nb_pages = max(int(search_serie['total_pages']), int(search_movie['total_pages']))
        return list_series, list_movies, nb_pages


    """
    Cette methode permet d'avoir les genres associes a un film ou une serie
    """
    @staticmethod
    def get_genre(media):
        media_genre = requests.get(f"{Api.base_url_start}genre/{media}/list{Api.base_url_end}").json()['genres']
        return media_genre

    """
    Cette methode permet d'obtenir les films ou les series associes au genre "genre"
    """
    @staticmethod
    def discover(media, id_genre, page):
        url = f"{Api.base_url_start}discover/{media}{Api.base_url_end}" \
              f"&with_genres={id_genre}&sort_by=popularity.desc&page={page}"
        request = requests.get(url).json()
        list_media = request['results']
        nb_pages = int(request['total_pages'])
        return list_media, nb_pages

    """
    Cette methode permet d'obtenir l'objet episode associe a l'ID de la serie "id_serie", au numero de la saison "season"
    et au numero de l'episode "episode_number"
    """
    @staticmethod
    def get_episode(id_serie, season, episode_number):
        request_episode = requests.get(f"{Api.base_url_start}tv/{id_serie}/season/{season}/episode/{episode_number}"\
                f"{Api.base_url_end}")
        episode_json = request_episode.json()
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
        request = requests.get(f"{Api.base_url_start}{media_type}/{id}/similar{Api.base_url_end}")
        similar_json = request.json()
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
        return media_list

    """
    Cette methode est appelee au moment du login de l'utilisateur pour lui donner un session ID necessaire
    a ce qu'il puisse noter un film ou une serie
    """
    @staticmethod
    def new_session():
        request = requests.get(f"{Api.base_url_start}authentication/guest_session/new?api_key={Api.api_key}")
        session = request.json()['guest_session_id']
        return session

    """
    Cette methode permet d'envoyer une note a themoviedb pour le film ou la serie d'ID "id"
    """
    @staticmethod
    def rate(id, grade, media, session):
        request = requests.post(f"{Api.base_url_start}{media}/{id}/rating?api_key={Api.api_key}" \
                                f"&guest_session_id={session}", params={"value": int(grade)}, headers={"Content-Type": "application/json;charset=utf-8"})
        return request.json()


    """
    Cette methode permet d'obtenir les films ou les series les mieux notes de la page "page"
    """
    @staticmethod
    def get_top_rated(media, page):
        result = requests.get(f"{Api.base_url_start}{media}/top_rated{Api.base_url_end}&"
                                  f"sort_by=vote_average.desc&page={page}").json()
        print(f"{Api.base_url_start}{media}/top_rated{Api.base_url_end}&"
                                  f"sort_by=vote_average.desc&page={page}")
        return result['results'], result['total_pages']
        
import requests
from classes.movie import Movie
from classes.Serie import Serie
from classes.episode import Episode
