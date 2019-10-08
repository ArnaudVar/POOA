from Exception import SetterException
from media import Media


class Serie(Media):
    """
    Cette classe permet de rassembler les différentes informations sur les séries
    """
    def __init__(self, id, name, description, cast, grade, genre, image, seasons, latest, date):
        """
        Constructeur de notre classe Serie, on considère que toutes les informations sont données par l'API lors de la
        construction d'une nouvelle série
        :param id: identifiant de la serie
        :param genre: genre de la série
        :param seasons: liste des saisons de la série
        :param latest: dernier épisode sortie de la série
        :param date: date de diffusion du prochain épisode de la série
        """
        Media.__init__(self,name,description,cast,grade,image)
        self._id = id
        self._genre = genre
        self.seasons = seasons
        self.latest = latest
        self.date = date

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
