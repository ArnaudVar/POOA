from Serie import Serie
from Exception import SetterException

class User :

    """
    Cette classe décrit l'utilisateur du site web
    Il est défini par son nom, son prénom, son ID, son mot de passe, et les séries qu'il regarde, stockées dans un dictionnaire
    """
    __id = 0
    def __init__(self, name, surname, password):

        """
        Constructeur de notre classe user
        :param id: l'identifiant private de notre classe, elle est private et sans mutateur
        :param password: le mot de passe de l'utilisateur, il est private
        :param series: le dictionnaire des séries regardées par notre utilisateur avec comme
        clé l'ID de la série et comme valeurs les derniers épisodes regardés, elle est private
        :param name: le prenom de l'utilsateur qui est private
        :param surname: le nom de l'utilsateur qui est private
        """
        self.__id = User.__id
        self.__password = password
        self.series = {}
        self.__name = name
        self.__surname = surname

    def _get_password(self):
        """
        Méthode appelée lorsqu'on voudra accéder au mot de passe utilisateur
        :return: renvoie le mot de passe
        """
        return self.__password

    def _get_name(self):
        """
        Méthode appelée lorsqu'on voudra accéder au prénom de l'utilisateur
        :return: renvoie le prénom de l'utilisateur
        """
        return self.name

    def _get_surname(self):
        """
        Méthode appelée lorsqu'on voudra accéder au nom de l'utilisateur
        :return: renvoie le nom de l'utilisateur
        """
        return self.surname

    def _get_id(self):
        """
        Méthode appelée lorsqu'on voudra accéder à l'ID de l'utilisateur
        :return: renvoie l'ID de l'utilisateur
        """
        return self.__id

    def _set_password(self, password):
        self.__password = password

    def _set_name(self, name):

        """
        Méthode appelée lorsque l'on veut modifier le prénom de l'utilisateur

        :return: None (on ne peut pas changer le nom de l'utilisateur)
        """
        return SetterException("On ne peut pas changer le nom de l'utilisateur")

    def _set_surname(self, surname):

        """
        Méthode appelée lorsque l'on veut modifier le nom de l'utilisateur

        :return: None (on ne peut pas changer le nom de l'utilisateur)
        """

        return SetterException("On ne peut pas changer le nom de l'utilisateur")

    def _set_id(self, id):


        """
        Méthode appelée lorsque l'on veut modifier l'ID de l'utilisateur

        :return: None (on ne peut pas changer l'ID de l'utilisateur)
        """
        return SetterException("On ne peut pas changer l'ID de l'utilisateur")
    id = property(_get_id,_set_id)
    name = property(_get_name, _set_name)
    surname = property(_get_surname,_set_surname)
    password = property(_get_password, _set_password)


    def add_serie(self, serie):

        """
        Méthode appelée lorsque l'on veut ajouter une série au dictionnaire des séries que regarde l'utilisateur

        :return: None (type void)
        """
        self.series[serie.getId()] = 'S1E1'

    def remove_serie(self, serie):

        """
        Méthode appelée lorsque l'on veut enlever une série au dictionnaire des séries que regarde l'utilisateur
        lorsqu'il ne veut plus la regarder
        :return: None (type void)
        """
        del self.series[serie.getId()]

    def next_episode(self,serie):

        """
        Méthode appelée pour une série lorsque l'utilisateur a regardé un épisode et qu'il veut passer au suivant

        :return: None (type void)
        """
        if serie.getId() not in self.series.keys() :
            raise ValueError("Série non commencée")
        else :

            if self.series[serie.id] == serie.latest :
                print("Vous êtes rendus au dernier épisode en date")
            else :
                separation = self.series[serie.getId()].split('E')
                number_season = int(separation[0].split('S')[1])
                number_episode = separation[1]
                number_episode= int(number_episode)
                if number_episode == len(serie.seasons[number_season-1].episodes) :
                    self.series[serie.getId()] = 'S'+ str(number_season + 1) +'E1'
                else :
                    self.series[serie.getId()] = separation[0] + 'E' + str(number_episode + 1)


