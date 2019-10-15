from classes.Exception import SetterException
from classes.media import Media


class Episode(Media):

    def __init__(self, id,  name, description, cast, grade, image, id_serie, num_season, num_episode, release):
        Media.__init__(self, name, description, grade, image)

        self._id_serie = id_serie
        self.num_season = num_season
        self.num_episode = num_episode
        self.release = release
        self.cast = cast
        self._id=f"S{num_season}E{num_episode}"

    def __repr__(self):
        return self.name

    def _get_id_serie(self):
        """
        Méthode appelée lorsque l'on veut accéder à l'identifiant de la série de l'épisode
        :return: int : l'identifiant de la série de laquelle est issu l'épisode
        """
        return self._id_serie

    def _set_id_serie(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier l'identifiant de la série de l'épisode

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')
