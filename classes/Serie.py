from Exception import SetterException


class Serie():
    """
    Cette classe permet de rassembler les différentes informations sur les séries
    """
    def __init__(self, id, name, description, cast, grade, genre, image, seasons, latest, date):
        """
        Constructeur de notre classe Serie, on considère que toutes les informations sont données par l'API lors de la
        construction d'une nouvelle série
        :param id: identifiant de la serie
        :param name: nom de la serie
        :param description: description de la serie
        :param cast: cast de la série
        :param grade: note de la série
        :param genre: genre de la série
        :param image: image de couverture de la série
        :param seasons: liste des saisons de la série
        :param latest: dernier épisode sortie de la série
        :param date: date de diffusion du prochain épisode de la série
        """
        self._id = id
        self._name = name
        self._description = description
        self.cast = cast
        self.grade = grade
        self._genre = genre
        self._image = image
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

    def _get_name(self):
        """
        Méthode appelée lorsque l'on veut accéder au nom de la série
        :return: str : le nom de la série
        """
        return self._name

    def _set_name(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier le nom de la série

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    def _get_description(self):
        """
        Méthode appelée lorsque l'on veut accéder à la description de la série
        :return: str : la description de la série
        """
        return self._description

    def _set_description(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier la description de la série

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

    def _get_image(self):
        """
        Méthode appelée lorsque l'on veut accéder à l'image de la série
        :return: l'image de la série
        """
        return self._image

    def _set_image(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier l'image de la série

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    id = property(_get_id,_set_id)
    name = property(_get_name, _set_name)
    description = property(_get_description,_set_description)
    genre = property(_get_genre, _set_genre)
    image = property(_get_image, _set_image)

    def numberSeasons(self):
        """
        Méthode appelée pour avoir le nombre de saisons d'une série
        :return: int : le nombre de saisons
        """
        return len(self.seasons)
