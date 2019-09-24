from Exception  import SetterException, AttributeException

class Season :
    """
    Cette classe permet de rassembler les différentes informations sur les saisons
    On y trouve les identifiants uniques des saisons, leurs informations principales (numéro saison, liste d'épisodes,
    description de la saison, cast, notes, image
    """

    def __init__(self, id, listEpisodes, cast, grade, image):
        """
        Constructeur de notre classe saison, on considère que toutes les informations sont données par l'API lors de la
        construction d'une nouvelle série
        :param id: l'identifiant private de notre classe, elle est private et sans mutateur
        :param listEpisodes: la liste d'épisodes de notre classe, elle est private
        :param cast: le cast de la saison, il est private
        :param notes: les notes données par les utilisateurs, elles sont private
        :param image: l'image de la saison qui est private
        """
        self._id = id
        self._listEpisode = listEpisodes
        self.cast = cast
        self.grade = grade
        self._image = image

    def numberEpisodePlanned(self):
        """
        Méthode renvoyant le nombre d'épisodes prévus dans la saison
        :return: int
        """
        return len(self.listEpisode)

    def _get_listEpisode(self):
        """
        Méthode appelée lorsqu'on voudra accéder à la liste d'épisodes de la saison
        ELle renvoie la liste des épisodes de la saison pour cette série
        :return: liste d'objets episodes
        """
        return self._listEpisode

    def _set_listEpisode(self, *args):
        """
        Setter de la liste d'épisodes
        Elle renvoie une exception lorsqu'elle est invoquée, en effet ici on considère qu'on ne pourra pas changer toute la liste
        d'épisodes d'un coup mais plutôt en rajouter au fure et à mesure
        :param args: paramètres passés lors de l'appel
        :return: None
        """
        raise SetterException("l'attribu listEpisode de la classe Season ne possède pas de setter,\n \
                              essayez plutôt d'ajouter un épisode avec la méthode addEpisode")

    def _get_image(self):
        """
        Méthode appelée lorsqu'on voudra accéder à l'image de la saison
        :return: image
        """
        return self._image

    def _set_image(self, image):
        """
        méthode appelée lorsqu'on veut changer la valeur de l'image de la saison
        :param note: la nouvelle image de la saison
        :return: None
        """
        return self._image

    def _get_id(self):
        """
        Méthode appelée lorsqu'on voudra accéder à l'id de la saison
        :return: int
        """

        return self._id

    def _set_id(self, *args):
        """
        méthode appelée lorsqu'on veut changer la valeur de l'id de la saison
        Ici l'id ne peut être modifié. En effet, on veut que l'id de la série soit unique
        :param args: paramètre donné comme nouvelle valeur de id
        :return: None
        """

        raise SetterException("l'attribu id de la classe Season n'est pas modifiable")

    id = property(_get_id, _set_id)
    image = property(_get_image, _set_image)
    listEpisode = property(_get_listEpisode, _set_listEpisode)


s1 = Season(3, ["e1","e2"], "cast", 3.5, "image")





