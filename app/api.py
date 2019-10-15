import requests
from classes.movie import Movie
from classes.Serie import Serie


class Api:

    api_key = "11893590e2d73c103c840153c0daa770"
    base_url_serie = "https://api.themoviedb.org/3/tv/"
    base_url_movie = "https://api.themoviedb.org/3/movie/"
    base_url_end = f"?api_key={api_key}&language=en-US"

    @staticmethod
    def get_movie(id):

        r = requests.get(f"{Api.base_url_movie}{id}{Api.base_url_end}").json()
        genre_list = []
        for x in r['genres']:
            genre_list.append(x['name'])
        return Movie(id=r['id'], name=r['title'], description=r['overview'], grade=r['vote_average'],
                     image=r['poster_path'], genres=genre_list, date=r['release_date'])

    @staticmethod
    def get_serie(id):
        seriejson = requests.get(f"{Api.base_url_serie}{id}{Api.base_url_end}").json()
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
        return serie

    @staticmethod
    def get_popular():
        seriesjson = requests.get(f"{Api.base_url_serie}popular{Api.base_url_end}").json()
        moviesjson = requests.get(f"{Api.base_url_movie}popular{Api.base_url_end}").json()
        return seriesjson['results'], moviesjson['results']
