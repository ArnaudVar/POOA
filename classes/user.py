from serie import Serie
from Exception import SetterException

class User :
    __id = 0
    def __init__(self, name, surname, password):
        self.__id = User.__id
        self.__password = password
        self.series = {}
        self.__name = name
        self.__surname = surname

    def getName(self):
        return self.name

    def getSurname(self):
        return self.surname

    def setName(self):
        return SetterException()

    def setSurname(self):
        return SetterException()

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id

    def add_serie(self, serie):
        self.series[serie.getId()] = 'S1E1'

    def remove_serie(self, serie):
        del self.series[serie.getId()]

    def next_episode(self,serie):
        if serie.getId() not in self.series.keys() :
            raise ValueError("Série non commencée")
        else :
            separation = self.series[serie.getId()].split('E')
            number_season = int(separation[0].split('S')[1])
            number_episode = separation[1]
            number_episode= int(number_episode)
            if number_episode == len(serie.seasons[number_season-1].episodes) :
                self.series[serie.getId()] = 'S'+ str(number_season + 1) +'E1'
            else :
                self.series[serie.getId()] = separation[0] + 'E' + str(number_episode + 1)


