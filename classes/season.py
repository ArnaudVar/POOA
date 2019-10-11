from classes.Exception import SetterException, AttributeException
import requests
from classes.episode import Episode

class Season :
    """
    Cette classe permet de rassembler les différentes informations sur les saisons
    On y trouve les identifiants uniques des saisons, leurs informations principales (numéro saison, liste d'épisodes,
    description de la saison, cast, notes, image
    """

    def __init__(self, id, id_serie ,season_number,episode_count, listEpisodes, grade, image):
        """
        Constructeur de notre classe saison, on considère que toutes les informations sont données par l'API lors de la
        construction d'une nouvelle série
        :param id: l'identifiant private de notre classe, elle est private et sans mutateur
        :param episode_count: le nombre d'épisodes de notre saison, elle est private
        :param episode: le dictionnaire qui permet de stocker les épisodes déjà consultés pour la saison
        :param notes: les notes données par les utilisateurs, elles sont private
        :param image: l'image de la saison qui est private
        """
        self.id_serie = id_serie
        self._id = id
        self.episode_count = episode_count
        self.season_number = season_number
        self._listEpisode = listEpisodes
        self.grade = grade
        self._image = image
        self.selected_episode = self.get_selected_episode(1)

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

    def get_selected_episode(self, i):
        request_episode = requests.get("https://api.themoviedb.org/3/tv/" + str(self.id_serie)+"/season/"+ str(self.season_number) +"/episode/" + str(i) + "?api_key=11893590e2d73c103c840153c0daa770&language=en-US")
        episode_json = request_episode.json()
        episode = Episode(episode_json['name'], episode_json["overview"], episode_json["guest_stars"], episode_json["vote_average"], episode_json["still_path"], self.id_serie, self.season_number, i, episode_json["air_date"])
        return episode
    id = property(_get_id, _set_id)
    listEpisode = property(_get_listEpisode, _set_listEpisode)






