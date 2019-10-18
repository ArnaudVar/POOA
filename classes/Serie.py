from classes.Exception import SetterException
from classes.media import Media
import requests
from classes.episode import Episode
from app.api import Api


class Serie(Media):
    """
    Cette classe permet de rassembler les différentes informations sur les séries
    """
    def __init__(self, id, name, description, grade, genre, image, seasons, seasons_count, latest, date):
        """
        Constructeur de notre classe Serie, on considère que toutes les informations sont données par l'API lors de la
        construction d'une nouvelle série
        :param id: identifiant de la serie
        :param genre: genre de la série
        :param seasons: liste des saisons de la série
        :param latest: dernier épisode sortie de la série
        :param date: date de diffusion du prochain épisode de la série
        """
        Media.__init__(self,name,description, grade, image)
        self._id = id
        self._genre = genre
        self.seasons_count = seasons_count
        self.seasons = seasons
        self.latest = latest
        self.date = date
        self.selected_episode = 'S1E1'

    def _get_id(self):
        """
        Méthode appelée lorsque l'on veut accéder à l'identifiant de la série
        :return: int : l'identifiant de la série
        """
        return self._id

    def _set_id(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier l'identifiant de la série

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    def _get_genre(self):
        """
        Méthode appelée lorsque l'on veut accéder au genre de la série
        :return: str : le genre de la série
        """
        return self._genre

    def _set_genre(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier le genre de la série

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    id = property(_get_id,_set_id)
    genre = property(_get_genre, _set_genre)

    def numberSeasons(self):
        """
        Méthode appelée pour avoir le nombre de saisons d'une série
        :return: int : le nombre de saisons
        """
        return len(self.seasons)

    def set_selected_episode(self, i, j):
        self.selected_episode = 'S'+str(i)+'E'+str(j)

    def get_current_season(self):
        step1 = self.selected_episode.split('S')
        season = int(step1[1].split('E')[0])
        return(season)

    def get_current_episode(self):
        episode = int(self.selected_episode.split('E')[1])
        return(episode)

    @property
    def get_episode(self):
        return Api.get_episode(self.id, self.get_current_season(), self.get_current_episode())

